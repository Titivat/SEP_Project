from server.model import user

class UserController(object):

    def __init__(self, db):
        self.db = db

    def create_user(self, username, password):
        u = user.User(username=username, password=password)
        self.db.session.add(u)
        self.db.session.commit()
    
    def get_users(self):
        users = []
        for u in user.User.query.all():
            users.append(u.username)
        return users
