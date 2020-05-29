import logging
import msgpack
from .base import Session
from .model import User, Document
from .editsession import EditSession
import socketserver
import threading

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
                
                elif o["action"] == "add" and "id" in o:
                    # Add participants to document
                    docid = o["id"]
                    doc = db.query(Document).filter(Document.id==docid).first()
                    if not doc:
                        logging.error("document not found")
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "add", "err": "document not found"}))
                        continue
                    if self.user not in doc.participants:
                        doc.participants.append(self.user)
                    try:
                        db.commit()
                        self.request.sendall(msgpack.packb({"success": True, "ctx": "add", "id": docid, "name": doc.name}))
                    except Exception as e:
                        db.rollback()
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "add", "err": str(e)}))
                
                elif o["action"] == "remove" and "id" in o:
                    # Remove participants from document
                    docid = o["id"]
                    doc = db.query(Document).filter(Document.id==docid).first()
                    if not doc:
                        logging.error("document not found")
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "remove", "err": "document not found"}))
                        continue
                    if self.user in doc.participants:
                        doc.participants.remove(self.user)
                    try:
                        db.commit()
                        self.request.sendall(msgpack.packb({"success": True, "ctx": "remove", "id": docid, "name": doc.name}))
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
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "close"}))

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
