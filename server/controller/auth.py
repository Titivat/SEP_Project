from .. import db
from server.model import user

def validate_credentials(username, password):
    u = user.User.query.filter(user.User.username==username).first()
    if not u:
        return False
    return u.verify_password(password)
