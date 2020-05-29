import logging
import msgpack
from .base import Session
from .controller import AuthController, DocumentController, UserController
from .model import User, Document
import socketserver
import threading

class ThreadedTCPServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        """Initialize the server and keep a set of sessions."""
        super().__init__(server_address, RequestHandlerClass, True)
        self.sessions = dict()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
    
    def setup(self):
        super().setup()

        # Session for communicating with database
        self.db = Session()

        # Controllers
        self.authController = AuthController(self, self.db)
        self.documentController = DocumentController(self, self.db, self.authController, self.server.sessions)
        self.userController = UserController(self, self.db)

    def handle(self):

        # Buffer
        unpacker = msgpack.Unpacker()

        while True:

            try:
                buf = self.request.recv(1024**2)
                if not buf:
                    # Client closes socket
                    break
            except Exception as e:
                logging.error(e)
                break

            unpacker.feed(buf)

            for o in unpacker:
                if "action" not in o:
                    # No action, so skip it
                    continue

                if o["action"] == "register" and "username" in o and "password" in o:
                    # Register
                    username = o["username"]
                    password = o["password"]
                    self.userController.create_user(username, password)
                    continue

                if o["action"] == "login" and "username" in o and "password" in o:
                    # Login
                    username = o["username"]
                    password = o["password"]
                    self.authController.login(username, password)
                    continue

                if o["action"] == "logout":
                    # Logout user
                    self.authController.logout()
                    continue
                
                if o["action"] == "create" and "name" in o:
                    # Create document
                    name = o["name"]
                    self.documentController.create_document(name, self.authController.User())
                    continue
                
                if o["action"] == "delete" and "id" in o:
                    # Delete document
                    id = o["id"]
                    self.documentController.delete_document(id, self.authController.User())
                    continue
                
                if o["action"] == "documents":
                    # Retrieve documents for users
                    self.documentController.get_documents(self.authController.User())
                    continue
                
                if o["action"] == "shareddocuments":
                    # Retrieve shared documents for users
                    self.documentController.get_shareddocuments(self.authController.User())
                    continue
                
                if o["action"] == "add" and "id" in o:
                    # Add participants to document
                    id = o["id"]
                    self.documentController.add_participant(id, self.authController.User())
                    continue
                
                if o["action"] == "remove" and "id" in o:
                    # Remove participants from document
                    id = o["id"]
                    self.documentController.remove_participant(id, self.authController.User())
                    continue
                
                if o["action"] == "open" and "id" in o:
                    # Open document
                    id = o["id"]
                    self.documentController.open(id)
                    continue

                if o["action"] == "text":
                    # Retrieve content of document
                    self.documentController.text()
                    continue
                
                if o["action"] == "edit" and "patch" in o:
                    # Updating text
                    patch = o["patch"]
                    self.documentController.edit(patch)
                    continue

                if o["action"] == "execute":
                    # Execute script
                    self.documentController.execute()
                    continue

                if o["action"] == "close":
                    # Close
                    self.documentController.close()
                    continue
    
    def finish(self):
        super().finish()

        if self.documentController.has_session():
            # unregister when client closes
            self.documentController.close()
        
        self.db.close()

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
