from server.model import user, document

class DocumentController(object):

    def __init__(self, db):
        self.db = db

    def create_document(self, name, owner):
        u = user.User.query.filter(user.User.username==owner).first()
        doc = document.Document(name=name, owner=u)
        self.db.session.add(doc)
        self.db.session.commit()

    def remove_document(self, id, owner):
        document.Document.query.filter(document.Document.id==id, document.Document.user_owner==owner).delete()
        self.db.session.commit()

    def rename_document(self, id, owner, name):
        doc = document.Document.query.filter(document.Document.id==id, document.Document.user_owner==owner).first()
        doc.name = name
        self.db.session.commit()
    
    def get_documents(self, owner):
        docs = []
        for d in document.Document.query.all():
            docs.append({"id": d.id, "name": d.name})
        return docs
