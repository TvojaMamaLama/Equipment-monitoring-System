from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    login: str
    user_uid: str


class UserCreate(BaseModel):
    login: str
    password: str

