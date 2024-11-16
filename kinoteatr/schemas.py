from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional, List


class CommentCreate(BaseModel):
    text: str


class Comment(BaseModel):
    id: int
    text: str
    created_at: datetime
    user_username: str

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
    comment: List[Comment]

    class Config:
        orm_mode = True








