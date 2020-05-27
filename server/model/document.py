import datetime
from ..base import Base
from sqlalchemy import Column, String, Integer, Binary, DateTime, ForeignKey, UniqueConstraint

class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(), nullable=False)
    user_owner = Column(String(), ForeignKey('user.username'), nullable=False)
    content = Column(Binary())
    updated_date = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('name', 'user_owner', name='user_documents'),
    )
