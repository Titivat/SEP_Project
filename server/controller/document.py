from .. import db
from server.model import user, document

def create_document(name, owner):
    u = user.User.query.filter(user.User.username==owner).first()
    doc = document.Document(name=name, owner=u)
    db.session.add(doc)
    db.session.commit()

def remove_document(id, owner):
    document.Document.query.filter(document.Document.id==id, document.Document.user_owner==owner).delete()
    db.session.commit()

def rename_document(id, owner, name):
    doc = document.Document.query.filter(document.Document.id==id, document.Document.user_owner==owner).first()
    doc.name = name
    db.session.commit()
