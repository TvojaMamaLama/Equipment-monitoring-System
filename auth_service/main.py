import uuid
import datetime
from typing import List, Optional

from fastapi import FastAPI, Depends, status, Header, Security, Response
from fastapi.exceptions import HTTPException

from models import database
import settings
from auth import authenticate_user, create_access_token
import crud
import schemas


app = FastAPI()
app.state.database = database


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


@app.post("/auth")
async def user_authorization(authorization: Optional[str] = Header(None)):
    if authorization:
        login_password: list[str] = authorization[7:-1].split(":")
        user = schemas.UserAuthenticate(login=login_password[0], password=login_password[1])
        print(user)
    else:
        return Response(status_code=400, content={"message": "put your login and password to auth header"})
    user = await authenticate_user(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    scopes = ["user"]
    if user.is_admin:
        scopes.append("admin")
    access_token = create_access_token(
        data={"user": user.login, "scopes": scopes},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users", response_model=List[schemas.UserResponse])
async def get_all_users_view():
    return await crud.get_all_users()


@app.post("/users", response_model=schemas.UserResponse)
async def create_user_view(user: schemas.UserCreate):
    response_user = await crud.create_user(user)
    return response_user


@app.get("/users/{user_uid}", response_model=schemas.UserResponse)
async def get_user_uid(user_uid: uuid.UUID):
    return await crud.get_user_by_uid(user_uid)


# @app.post("/token", response_model=schemas.Token)
# async def login_for_access_token(user: schemas.UserAuthenticate):
#     user = auth.authenticate_user(user)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     scopes = ["user"]
#     if user.is_admin:
#         scopes.append("admin")
#     access_token = auth.create_access_token(
#         data={"user": user.login, "scopes": scopes},
#         expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
