from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field,Relationship
from typing import Optional, List

class Blog(Base):
    __tablename__ = "Blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="blogs")

class User(Base):
    __tablename__ =  "users"
    id = Column(Integer, primary_key=True, index=True)      
    name = Column(String, nullable=False)   
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    blogs=relationship("Blog",back_populates="creator") 



