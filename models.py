from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
# from sqlmodel import SQLModel, Field,Relationship
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



# class Blog(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     title: str = Field(nullable=False)
#     body: str = Field(nullable=False)
#     user_id: int = Field(foreign_key="users.id")
#     creator: "User" = Relationship(back_populates="blogs")

# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str = Field(nullable=False)
#     email: str = Field(nullable=False)
#     password: str = Field(nullable=False)
#     blogs: List[Blog] = Relationship(back_populates="creator")