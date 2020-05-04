import datetime
from .. import db

class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    user_owner = db.Column(db.String, db.ForeignKey('user.username'))
    content = db.Column(db.Binary)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
