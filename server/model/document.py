import datetime
from ..base import Base
from sqlalchemy import Column, String, Integer, Binary, DateTime, ForeignKey

class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_owner = Column(String, ForeignKey('user.username'))
    content = Column(Binary)
    updated_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
