from .. import db
from server.model import user, document

def create_document(name, owner):
    u = user.User.query.filter(user.User.username==owner).first()
    doc = document.Document(name=name, owner=u)
    db.session.add(doc)
    db.session.commit()
