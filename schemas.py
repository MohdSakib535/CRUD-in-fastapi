"""
we use schema  for validationand and formatting response data
"""
from pydantic import BaseModel
from typing import Optional,List


class Blog(BaseModel):
    title: str
    body: str

    class Config():
        from_attributes =True

class ShowUser(BaseModel):
    id :int
    name: str
    email: str
    blogs:List[Blog]=[]

    class Config():
        from_attributes = True



class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    creator: Optional[ShowUser]

    class Config():
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str


class Login(BaseModel):
    username: str
    password: str

    class Config():
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    email: Optional[str] = None


