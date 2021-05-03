import uuid
from typing import List

from pydantic import BaseModel, validator

import models


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

    @validator("login")
    def login_length(cls, login):
        if len(login) > 50 or len(login) < 5:
            raise ValueError("login max len 50, min len 5")
        return login


class UserAuthenticate(BaseUser):
    pass
