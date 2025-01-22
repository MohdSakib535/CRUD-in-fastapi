from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class Blog(Base):
    __tablename__ = "Blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)

class User(Base):
    __tablename__ =  "users"
    id = Column(Integer, primary_key=True, index=True)      
    name = Column(String, nullable=False)   
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)