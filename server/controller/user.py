from .. import db
from server.model import user

def create_user(username, password):
    u = user.User(username=username, password=password)
    db.session.add(u)
    db.session.commit()
