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
                    continue
                if o["action"] == "register" and "username" in o and "password" in o:
                    username = o["username"]
                    password = o["password"]
                    user = User(username=username, password=password)
                    session.add(user)
                    self.request.sendall(msgpack.packb({"success": True}))
                elif o["action"] == "login" and "username" in o and "password" in o:
                    username = o["username"]
                    password = o["password"]
                    user = session.query(User).filter(User.username==username).first()
                    if not user:
                        logging.error("user not found")
                        self.request.sendall(msgpack.packb({"success": False, "err": "user not found"}))
                        continue
                    if not user.verify_password(password):
                        logging.error("wrong password")
                        self.request.sendall(msgpack.packb({"success": False, "err": "wrong password"}))
                        continue
                    logging.info("correct password")
                    self.request.sendall(msgpack.packb({"success": True}))

            session.commit()
    
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
