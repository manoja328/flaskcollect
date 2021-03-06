from flask import session
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from tabledef import *
import bcrypt

@contextmanager
def session_scope():
  """Provide a transactional scope around a series of operations."""
  s = get_session()
  s.expire_on_commit = False
  try:
    yield s
    s.commit()
  except:
    s.rollback()
    raise
  finally:
    s.close()

def get_session():
  return sessionmaker(bind=engine)()

def get_user():
  username = session['username']
  with session_scope() as s:
    user = s.query(User).filter(User.username.in_([username])).first()
    return user

def add_user(username, password, email):
  with session_scope() as s:
    u = User(username=username, password=password, email=email)
    s.add(u)
    s.commit()


def add_qa(filename,question, answer):
  with session_scope() as s:
    #username = 'random'
    username = session['username']
    u = Complex(filename=filename,question=question,answer=answer,annotator=username)
    s.add(u)
    s.commit()
    
def get_qa(filename):
  with session_scope() as s:
    qas = s.query(Complex).filter(Complex.filename.in_([filename])).all()
    return qas


def get_fnames():   
    with session_scope() as s:
        qas = s.query(Complex).all()
        return qas


def get_fnames_good():   
    with session_scope() as s:
        #session.query(func.count(User.name), User.name).group_by(User.name).all()
        qas = s.query( Complex.filename,func.count(Complex.filename)).group_by(Complex.filename).all()
        #qas = (Complexfunc.count(User.name)).all()
        return qas

def change_user(**kwargs):
  username = session['username']
  with session_scope() as s:
    user = s.query(User).filter(User.username.in_([username])).first()
    for arg, val in kwargs.items():
      if val != "":
        setattr(user, arg, val)
    s.commit()

def hash_password(password):
  return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

def credentials_valid(username, password):
  with session_scope() as s:
    user = s.query(User).filter(User.username.in_([username])).first()
    if user:
      return bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8'))
    else:
      return False

def username_taken(username):
  with session_scope() as s:
    return s.query(User).filter(User.username.in_([username])).first()
