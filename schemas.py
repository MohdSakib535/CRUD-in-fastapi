"""
we use schema  for validationand and formatting response data
"""
from pydantic import BaseModel
from typing import Optional,List


class Blog(BaseModel):
    title: str
    body: str


class ShowUser(BaseModel):
    id :int
    name: str
    email: str

    class Config():
        from_attributes = True

    class Config():
        from_attributes =True


class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    user_id : int|None
    creator :ShowUser

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


