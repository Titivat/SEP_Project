import logging
import msgpack
from .base import Session
from .model import User, Document
import socketserver
import threading

class ThreadedTCPServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        """Initialize the server and keep a set of registered clients."""
        super().__init__(server_address, RequestHandlerClass, True)
        self.clients = set()
    
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
        session = Session()
        unpacker = msgpack.Unpacker()
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
                    session.add(user)
                    try:
                        session.commit()
                        self.request.sendall(msgpack.packb({"success": True, "ctx": "register"}))
                    except Exception as e:
                        session.rollback()
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "register", "err": str(e)}))
                    continue

                elif o["action"] == "login" and "username" in o and "password" in o:
                    # Login
                    username = o["username"]
                    password = o["password"]
                    user = session.query(User).filter(User.username==username).first()
                    if not user:
                        logging.error("user not found")
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "login", "err": "user not found"}))
                        continue
                    if not user.verify_password(password):
                        logging.error("wrong password")
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "login", "err": "wrong password"}))
                        continue
                    logging.info("correct password")
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "login"}))
                    self.user = user
                    continue

                if not self.user:
                    # Not login just pass
                    self.request.sendall(msgpack.packb({"success": False, "ctx": "session", "err": "user not logged in"}))
                    continue

                if o["action"] == "logout":
                    # Logout user
                    self.user = None
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "logout"}))
                    continue
                
                elif o["action"] == "users":
                    # Retrieve users
                    users = []
                    for u in session.query(User).filter(User.username!=self.user.username):
                        users.append(u.username)
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "users", "users": users}))
                
                elif o["action"] == "create" and "name" in o:
                    # Create document
                    name = o["name"]
                    if name.strip() == "":
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "create", "err": "document name cannot be empty"}))
                        continue
                    doc = Document(name=name, owner=self.user)
                    session.add(doc)
                    try:
                        session.commit()
                        self.request.sendall(msgpack.packb({"success": True, "ctx": "create", "id": doc.id, "name": doc.name}))
                    except Exception as e:
                        session.rollback()
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "create", "err": str(e)}))
                
                elif o["action"] == "delete" and "id" in o:
                    # Delete document
                    docid = o["id"]
                    session.query(Document).filter(Document.id==docid).delete()
                    try:
                        session.commit()
                        self.request.sendall(msgpack.packb({"success": True, "ctx": "delete"}))
                    except Exception as e:
                        session.rollback()
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "delete", "err": str(e)}))
                
                elif o["action"] == "documents":
                    # Retrieve documents for users
                    docs = []
                    for d in session.query(Document).filter(Document.owner==self.user).all():
                        docs.append({"id": d.id, "name": d.name})
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "documents", "documents": docs}))
                
                elif o["action"] == "shareddocuments":
                    # Retrieve shared documents for users
                    docs = []
                    for d in session.query(Document).join((Document.participants, User)).filter(User.username==self.user.username).all():
                        docs.append({"id": d.id, "name": d.name})
                    self.request.sendall(msgpack.packb({"success": True, "ctx": "shareddocuments", "documents": docs}))
                
                elif o["action"] == "add" and "id" in o and "participants" in o:
                    # Add participants to document
                    docid = o["id"]
                    participants = o["participants"]
                    doc = session.query(Document).filter(Document.id==docid).first()
                    if not doc:
                        logging.error("document not found")
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "add", "err": "document not found"}))
                        continue
                    users = session.query(User).filter(User.username.in_(participants)).all()
                    for u in users:
                        if u is not doc.owner and u not in doc.participants:
                            doc.participants.append(u)
                    try:
                        session.commit()
                        self.request.sendall(msgpack.packb({"success": True, "ctx": "add"}))
                    except Exception as e:
                        session.rollback()
                        self.request.sendall(msgpack.packb({"success": False, "ctx": "add", "err": str(e)}))

        session.close()
    
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
