from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

engine = create_engine("sqlite:///storage.db", echo=True)

_Session = sessionmaker(bind=engine)

Base = declarative_base()

def Session():
    return _Session()

def SafeSession():
    return scoped_session(_Session)()
