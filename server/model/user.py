import datetime
from .. import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from .document import Document

access = db.Table('access',
    db.Column('document_id', db.Integer, db.ForeignKey('document.id'), primary_key=True),
    db.Column('username', db.String, db.ForeignKey('user.username'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'

    username = db.Column(db.String, primary_key=True)
    _password = db.Column(db.Binary)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    documents = db.relationship('Document', backref='owner')
    participations = db.relationship('Document', secondary=access, backref=db.backref('participants', lazy='dynamic'))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext, 10)

    def verify_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)
