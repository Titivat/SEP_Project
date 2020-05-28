import datetime
from ..base import Base
from sqlalchemy import Column, String, Integer, Binary, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
import uuid

def generate_uuid():
    return uuid.uuid4().hex

class Document(Base):
    __tablename__ = 'document'

    id = Column(String(32), primary_key=True, default=generate_uuid)
    name = Column(String(), nullable=False)
    user_owner = Column(String(), ForeignKey('user.username'), nullable=False)
    _content = Column(Binary())
    updated_date = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('name', 'user_owner', name='user_documents'),
    )

    @hybrid_property
    def content(self):
        if self._content:
            return self._content.decode('utf-8')
    
    @content.setter
    def content(self, text):
        self._content = text.encode('utf-8')
