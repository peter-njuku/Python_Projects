from sqlalchemy import Column,Integer,String,DateTime,Boolean
from database import Base

class Tasks(Base):
    __tablename__ = "todo"

    id=Column(Integer,primary_key=True,index=True)
    task=Column(String,index=True)
    completed=Column(Boolean,default=False)

class User(Base):
    __tablename__ ="users"

    id=Column(Integer, primary_key=True,index=True)
    email=Column(String, unique=True,index=True)
    hashed_password=Column(String)
    is_active=Column(Boolean, default=True)
