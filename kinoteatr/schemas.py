from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional


class CommentCreate(BaseModel):
    text: str
    username: str


class Comment(BaseModel):
    id: int
    text: str
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email:  EmailStr
    password1: str
    password2: str
    first_name: str
    last_name: Optional[str] = None


class UserAuth(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True



