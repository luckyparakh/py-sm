from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # it has default values as true, hence it is optional


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    created_at: datetime

    class config:
        orm_mode = True


class PostResponse(PostBase):
    created_at: datetime
    user_id: int
    user: UserResponse

    class config:
        orm_mode = True


class PostVoteOut(BaseModel):
    Posts: PostResponse
    votes: int

    class config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int]


class VoteBase(BaseModel):
    post_id: int
    vote_direction: Literal[-1, 1]


class VoteResponse(BaseModel):
    post_id: int
    user_id: int
