from sqlalchemy import Column, Integer, Date, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()

class Users(Base):
    __tablename__= 'Users'
    id = Column(Integer, primary_key=True)
    UId = Column(Integer)
    capital = Column(Integer)

class Incomes(Base):
    __tablename__="Incomes"
    id = Column(Integer, primary_key=True)
    UId = Column(Integer)
    data = Column(DateTime, default=datetime.now)
    sum = Column(Integer)
class Consumptions(Base):
    __tablename__="Cons"
    id = Column(Integer, primary_key=True)
    UId = Column(Integer)
    sum = Column(Integer)
    reason = Column(String(255))
    data = Column(DateTime, default=datetime.now)