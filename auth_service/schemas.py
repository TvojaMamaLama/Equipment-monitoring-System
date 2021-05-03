import uuid
from typing import List

from pydantic import BaseModel

class BaseUser(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: str
    scopes: List[str]


class UserResponse(BaseModel):
    uid: uuid.UUID
    login: str
    is_admin: bool

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class UserCreate(BaseUser):
    pass


class UserAuthenticate(BaseUser):
    pass
