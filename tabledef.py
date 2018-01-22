from settings import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine , func
from sqlalchemy import Column, Integer, String , Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def db_connect():
  """
  Performs database connection using database settings from settings.py.
  Returns sqlalchemy engine instance
  """
  return create_engine(SQLALCHEMY_DATABASE_URI)

class User(Base):
  __tablename__ = "user"

  id = Column(Integer, primary_key=True)
  username = Column(String(30), unique=True)
  password = Column(String(80))
  email = Column(String(50))

  def __repr__(self):
    return '<User %r>' % self.username

class File(Base):
  __tablename__ = "files"

  id = Column(Integer, primary_key=True)
  filename = Column(String(80))
  istrain = Column(Integer)

  def __repr__(self):
    return '<User {}>'.format(self.filename,self.annotcount)

class Complex(Base):
    
    __tablename__ = "complex"
    qid = Column(Integer, primary_key=True)
    filename = Column(String(80))
    question = Column(Text())
    answer = Column(String(5))
    question_type = Column(String(10))
    annotator = Column(String(80))
    
    def __str__(self):
        return ('[Qid %s , %s]' %(self.qid,self.question))

    def __repr__(self):
        return ('<Qid %r , %r>' %(self.qid,self.question))

engine = db_connect() # Connect to database
Base.metadata.create_all(engine) # Create models
