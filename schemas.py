"""
we use schema  for validationand and formatting response data
"""
from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(BaseModel):
    title: str
    body: str

    class Config():
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    id :int
    name: str
    email: str

    class Config():
        from_attributes = True