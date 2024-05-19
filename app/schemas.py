from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from enum import Enum


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut


    class config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]

class Vote(BaseModel):
    post_id: int
    dir: conint(strict=True,le=1) # type: ignore