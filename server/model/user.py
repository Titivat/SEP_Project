import datetime
from ..base import Base
import bcrypt
from sqlalchemy import Column, String, Integer, Binary, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from .document import Document

access = Table('access',
    Column('document_id', Integer, ForeignKey('document.id'), primary_key=True),
    Column('username', String, ForeignKey('user.username'), primary_key=True)
)

class User(Base):
    __tablename__ = 'user'

    username = Column(String, primary_key=True)
    _password = Column(Binary)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    documents = relationship('Document', backref='owner')
    participations = relationship('Document', secondary=access, backref=backref('participants', lazy='dynamic'))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.hashpw(plaintext, bcrypt.gensalt())

    def verify_password(self, plaintext):
        return bcrypt.checkpw(plaintext, self._password)
