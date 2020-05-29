from .response import Response
from server.model import User

class UserController(object):

    def __init__(self, socket, db):
        self.socket = socket
        self.db = db

    def create_user(self, username, password):
        response = Response("register")

        if username.strip() == "" or password.strip() == "":
            self.socket.request.sendall(response(False, err="username or password cannot be empty"))
            return
        user = User(username=username, password=password)
        self.db.add(user)
        try:
            self.db.commit()
            self.socket.request.sendall(response(username=user.username))
        except Exception as e:
            self.db.rollback()
            self.socket.request.sendall(response(False, err=str(e)))
