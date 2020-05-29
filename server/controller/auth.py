from .response import Response
from server.model import User

class AuthController(object):

    def __init__(self, socket, db):
        self.socket = socket
        self.db = db
        self.user = None

    def login(self, username, password):
        response = Response("login")

        user = self.db.query(User).filter(User.username==username).first()
        if not user:
            self.socket.request.sendall(response(False, err="user not found"))
            return
        if not user.verify_password(password):
            self.socket.request.sendall(response(False, err="wrong password"))
            return
        self.socket.request.sendall(response(username=user.username))
        self.user = user
    
    def logout(self):
        self.user = None

        response = Response("logout")

        self.socket.request.sendall(response())
    
    def loggedIn(self):
        response = Response("login")

        if self.user is None:
            self.socket.request.sendall(response(False, err="user not logged in"))
            return False
        return True
    
    def User(self):
        return self.user
