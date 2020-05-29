from .editsession import EditSession
from .response import Response
from server.model import User, Document

class DocumentController(object):

    def __init__(self, socket, db, auth, sessions):
        self.socket = socket
        self.db = db
        self.authController = auth
        self.sessions = sessions
        self.current_session = None

    def create_document(self, name, owner):
        response = Response("create")

        if not self.authController.loggedIn():
            return

        if name.strip() == "":
            self.socket.request.sendall(response(False, err="document name cannot be empty"))
            return
        doc = Document(name=name, owner=owner)
        self.db.add(doc)
        try:
            self.db.commit()
            self.socket.request.sendall(response(id=doc.id, name=doc.name))
        except Exception as e:
            self.db.rollback()
            self.socket.request.sendall(response(False, err=str(e)))

    def delete_document(self, id, owner):
        response = Response("delete")

        if not self.authController.loggedIn():
            return

        doc = self.db.query(Document).filter(Document.id==id, Document.user_owner==owner.username).first()
        if not doc:
            self.socket.request.sendall(response(False, err="document not found"))
            return
        doc.participants = []
        self.db.delete(doc)
        try:
            self.db.commit()
            self.socket.request.sendall(response(id=doc.id, name=doc.name))
        except Exception as e:
            self.db.rollback()
            self.socket.request.sendall(response(False, err=str(e)))
    
    def get_documents(self, owner):
        response = Response("documents")

        if not self.authController.loggedIn():
            return

        docs = []
        for d in self.db.query(Document).filter(Document.user_owner==owner.username).all():
            docs.append({"id": d.id, "name": d.name})
        self.socket.request.sendall(response(documents=docs))
    
    def get_shareddocuments(self, user):
        response = Response("shareddocuments")

        if not self.authController.loggedIn():
            return

        docs = []
        for d in self.db.query(Document).join((Document.participants, User)).filter(User.username==user.username).all():
            docs.append({"id": d.id, "name": d.name})
        self.socket.request.sendall(response(documents=docs))
    
    def add_participant(self, id, user):
        response = Response("add")

        if not self.authController.loggedIn():
            return

        doc = self.db.query(Document).filter(Document.id==id).first()
        if not doc:
            self.socket.request.sendall(response(False, err="document not found"))
            return
        if user is doc.owner:
            self.socket.request.sendall(response(False, err="user is owner"))
            return
        if user not in doc.participants:
            doc.participants.append(user)
        try:
            self.db.commit()
            self.socket.request.sendall(response(id=doc.id, name=doc.name))
        except Exception as e:
            self.db.rollback()
            self.socket.request.sendall(response(False, err=str(e)))
    
    def remove_participant(self, id, user):
        response = Response("remove")

        if not self.authController.loggedIn():
            return
        
        doc = self.db.query(Document).filter(Document.id==id).first()
        if not doc:
            self.socket.request.sendall(response(False, err="document not found"))
            return
        if user in doc.participants:
            doc.participants.remove(user)
        try:
            self.db.commit()
            self.socket.request.sendall(response(id=doc.id, name=doc.name))
        except Exception as e:
            self.db.rollback()
            self.socket.request.sendall(response(False, err=str(e)))
    
    def open(self, id):
        response = Response("open")

        if not self.authController.loggedIn():
            return

        doc = self.db.query(Document).filter(Document.id==id).first()
        if not doc:
            self.socket.request.sendall(response(False, "document not found"))
            return
        if self.current_session:
            self.current_session.unregister(self.socket)
        if id not in self.sessions:
            self.sessions[id] = EditSession(id)
        self.current_session = self.sessions[id]
        self.current_session.register(self.socket)
        self.socket.request.sendall(response(id=doc.id, name=doc.name, text=self.current_session.content()))
    
    def close(self):
        response = Response("close")

        if not self.has_session():
            return

        self.current_session.unregister(self.socket, self.db)
        self.current_session = None
        self.socket.request.sendall(response())
    
    def has_session(self):
        return self.current_session is not None
    
    def text(self):
        response = Response("text")

        if not self.has_session():
            return

        self.socket.request.sendall(response(text=self.current_session.content()))
    
    def edit(self, patch):
        if not self.has_session():
            return
        self.current_session.update_text(self.socket, patch)
    
    def execute(self):
        if not self.has_session():
            return
        self.current_session.execute(self.socket)
