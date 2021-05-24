import datetime
import uuid
from jose import jwt, JWTError
from typing import List

from fastapi import Request, Header, HTTPException, status

from settings import ALGORITHM, SECRET_KEY


def decode_token(token: str) -> (uuid.UUID, List[str], int):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user: uuid.UUID = uuid.UUID(payload.get("user"))
        scopes: List[str] = payload.get("scopes")
        expire: int = payload.get("exp")
    except (KeyError, JWTError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not valid token")
    return user, scopes, expire


class HTTPHeaderAuthentication:
    def __init__(self, *, scopes: List[str]):
        self.scopes = set(scopes)

    def __call__(self, request: Request, authorization: str = Header(None)) -> uuid.UUID:
        try:
            authorization = authorization.split(" ")
            if len(authorization) != 2 and authorization[0] != "Bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not valid header")
        except (IndexError, AttributeError):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not valid header")
        user, scopes, expire = decode_token(token=authorization[1])
        if expire < datetime.datetime.utcnow().timestamp():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        if not self.has_required_scope(scopes):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
        return user

    def has_required_scope(self, user_scopes: List[str]) -> bool:
        """Verify the user has the desired auth scope"""
        for scope in self.scopes:
            if scope not in user_scopes:
                return False
        return True
