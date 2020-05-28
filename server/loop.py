import datetime
import logging
import msgpack
from .base import Session
from .model import User, Document
from diff_match_patch import diff_match_patch
import os
import socketserver
import subprocess
import threading

class EditSession:
    """Session for handling document edit"""

    dmp = diff_match_patch()

    def __init__(self, docid):
        self.clients = set()
        self.db = Session()
        self.running = False
        self.doc = self.db.query(Document).filter(Document.id==docid).first()
    
    def register(self, socket):
        self.clients.add(socket)
    
    def unregister(self, socket):
        self.clients.remove(socket)
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
    
    def update_text(self, socket, patch):
        patches = EditSession.dmp.patch_fromText(patch)
        if not self.doc.content:
            text, _ = EditSession.dmp.patch_apply(patches, "")
        else:
            text, _ = EditSession.dmp.patch_apply(patches, self.doc.content)
        
        self.doc.content = text

        self.broadcast(socket, msgpack.packb({"ctx": "edit", "patch": patch}))
    
    def content(self):
        return self.doc.content
    
    def broadcast(self, socket, data, all=False):
        for client in self.clients:
            if not all:
                if client is socket:
                    continue
            client.request.sendall(data)

    def execute(self, socket):
        if self.running:
            return
        self.running = True

        filename = str(datetime.datetime.now().timestamp())+".py"
        with open(filename, "w") as f:
            f.write(self.doc.content)
        proc = subprocess.Popen(["python3", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        os.remove(filename)
        output = {"ctx": "execute"}
        if stdout:
            output["stdout"] = stdout.decode("utf-8")
        if stderr:
            output["stderr"] = stderr.decode("utf-8")
        
        self.broadcast(socket, msgpack.packb(output), all=True)

        self.running = False

class ThreadedTCPServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        """Initialize the server and keep a set of registered clients."""
        super().__init__(server_address, RequestHandlerClass, True)
        self.clients = set()
        self.sessions = dict()
    
    def add_client(self, client):
        """Register a client with the internal store of clients."""
        logging.info(f"Connection from {client.client_address} has been established")
        self.clients.add(client)
    
    def remove_client(self, client):
        """Remove a client from the store of clients."""
        logging.info(f"Connection from {client.client_address} has been dropped")
        self.clients.remove(client)

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.user = None
        super().__init__(request, client_address, server)
    
    def setup(self):
        super().setup()
        self.server.add_client(self)

    def handle(self):
        # Session to database
        db = Session()

        # Buffer
        unpacker = msgpack.Unpacker()

        # Edit session
        session = None

        while True:

            buf = self.request.recv(1024**2)
            if not buf:
                break

            unpacker.feed(buf)

            for o in unpacker:
                if "action" not in o:
                    # No action, so skip it
                    continue

                if o["action"] == "register" and "username" in o and "password" in o:
                    # Register user
                    username = o["username"]
                    password = o["password"]
                    if username.strip() == "" or password.strip() == "":
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "register", "err": "username or password cannot be empty"}))
                        continue
                    user = User(username=username, password=password)
                    db.add(user)
                    try:
                        db.commit()
                        self.request.sendall(msgpack.packb({"success": True, "ctx": "register", "username": user.username}))
                    except Exception as e:
                        db.rollback()
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "register", "err": str(e)}))
                    continue

                elif o["action"] == "login" and "username" in o and "password" in o:
                    # Login
                    username = o["username"]
                    password = o["password"]
                    user = db.query(User).filter(User.username==username).first()
                    if not user:
                        logging.error("user not found")
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "login", "err": "user not found"}))
                        continue
                    if not user.verify_password(password):
                        logging.error("wrong password")
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "login", "err": "wrong password"}))
                        continue
                    logging.info("correct password")
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "login", "username": user.username}))
                    self.user = user
                    continue

                if not self.user:
                    # Not login just pass
                    self.request.sendall(msgpack.packb({"success": False, "ctx": "login", "err": "user not logged in"}))
                    continue

                if o["action"] == "logout":
                    # Logout user
                    self.user = None
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "logout"}))
                    continue
                
                elif o["action"] == "users":
                    # Retrieve users
                    users = []
                    for u in db.query(User).filter(User.username!=self.user.username):
                        users.append(u.username)
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "users", "users": users}))
                
                elif o["action"] == "create" and "name" in o:
                    # Create document
                    name = o["name"]
                    if name.strip() == "":
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "create", "err": "document name cannot be empty"}))
                        continue
                    doc = Document(name=name, owner=self.user)
                    db.add(doc)
                    try:
                        db.commit()
                        self.request.sendall(msgpack.packb({"success": True, "ctx": "create", "id": doc.id, "name": doc.name}))
                    except Exception as e:
                        db.rollback()
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "create", "err": str(e)}))
                
                elif o["action"] == "delete" and "id" in o:
                    # Delete document
                    docid = o["id"]
                    doc = db.query(Document).filter(Document.id==docid, Document.user_owner==self.user.username).first()
                    if not doc:
                        logging.error("document not found")
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "delete", "err": "document not found"}))
                        continue
                    doc.participants = []
                    db.delete(doc)
                    try:
                        db.commit()
                        self.request.sendall(msgpack.packb({"success": True, "ctx": "delete", "id": doc.id, "name": doc.name}))
                    except Exception as e:
                        db.rollback()
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "delete", "err": str(e)}))
                
                elif o["action"] == "documents":
                    # Retrieve documents for users
                    docs = []
                    for d in db.query(Document).filter(Document.owner==self.user).all():
                        docs.append({"id": d.id, "name": d.name})
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "documents", "documents": docs}))
                
                elif o["action"] == "shareddocuments":
                    # Retrieve shared documents for users
                    docs = []
                    for d in db.query(Document).join((Document.participants, User)).filter(User.username==self.user.username).all():
                        docs.append({"id": d.id, "name": d.name})
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "shareddocuments", "documents": docs}))
                
                elif o["action"] == "add" and "id" in o and "participants" in o:
                    # Add participants to document
                    docid = o["id"]
                    participants = o["participants"]
                    doc = db.query(Document).filter(Document.id==docid, Document.user_owner==self.user.username).first()
                    if not doc:
                        logging.error("document not found")
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "add", "err": "document not found"}))
                        continue
                    users = db.query(User).filter(User.username.in_(participants)).all()
                    for u in users:
                        if u is not doc.owner and u not in doc.participants:
                            doc.participants.append(u)
                    try:
                        db.commit()
                        self.request.sendall(msgpack.packb({"success": True, "ctx": "add"}))
                    except Exception as e:
                        db.rollback()
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "add", "err": str(e)}))
                
                elif o["action"] == "remove" and "id" in o and "participants" in o:
                    # Remove participants from document
                    docid = o["id"]
                    participants = o["participants"]
                    doc = db.query(Document).filter(Document.id==docid, Document.user_owner==self.user.username).first()
                    if not doc:
                        logging.error("document not found")
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "remove", "err": "document not found"}))
                        continue
                    for participant in doc.participants:
                        if participant.username in participants:
                            doc.participants.remove(participant)
                    try:
                        db.commit()
                        self.request.sendall(msgpack.packb({"success": True, "ctx": "remove"}))
                    except Exception as e:
                        db.rollback()
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "remove", "err": str(e)}))
                
                elif o["action"] == "open" and "id" in o:
                    # Open document
                    docid = o["id"]
                    doc = db.query(Document).filter(Document.id==docid).first()
                    if not doc:
                        logging.error("document not found")
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "open", "err": "document not found"}))
                        continue
                    if session:
                        session.unregister(self)
                    if docid not in self.server.sessions:
                        self.server.sessions[docid] = EditSession(docid)
                    session = self.server.sessions[docid]
                    session.register(self)
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "open", "id": doc.id, "name": doc.name, "text": session.content()}))
                
                if not session:
                    # User has no edit session
                    self.request.sendall(msgpack.packb({"success": False, "ctx": "session", "err": "no edit session"}))
                    continue

                elif o["action"] == "text":
                    # Retrieve content of document
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "text", "text": session.content()}))
                
                elif o["action"] == "edit" and "patch" in o:
                    # Updating text
                    logging.info(f"{self.user.username} {o}")
                    session.update_text(self, o["patch"])

                elif o["action"] == "execute":
                    # Execute script
                    session.execute(self)

                elif o["action"] == "close":
                    # Close
                    session.unregister(self)
                    session = None

        if session:
            # unregister when client close
            session.unregister(self)
        
        db.close()
    
    def finish(self):
        super().finish()
        self.server.remove_client(self)

if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 5000

    with ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(f"Server loop running in thread: {server_thread.name}")
        server_thread.join()
        server.shutdown()
