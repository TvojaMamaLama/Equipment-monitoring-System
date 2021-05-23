import uuid
import datetime
from typing import List

from fastapi import FastAPI, status, Response
from fastapi.exceptions import HTTPException

import models
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


@app.post("/auth", response_model=schemas.Token)
async def user_authorization(user: schemas.UserAuthenticate):
    user: models.User = await authenticate_user(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    scopes = []
    if user.is_admin:
        scopes.append("admin")
    access_token = create_access_token(data={"user": str(user.uid), "scopes": scopes}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "Bearer"}


@app.get("/users", response_model=List[schemas.UserResponse])
async def get_all_users_view():
    return await crud.get_all_users()


@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_view(user: schemas.UserCreate):
    if await models.User.objects.get_or_none(login=user.login):
        raise HTTPException(status_code=422, detail="User with same login exist")
    response_user = await crud.create_user(user)
    return response_user


@app.get("/users/{user_uid}", response_model=schemas.UserResponse)
async def get_user_by_uid_view(user_uid: uuid.UUID):
    return await crud.get_user_by_uid(user_uid)


@app.patch("/users/{user_uid}", response_model=schemas.UserResponse)
async def update_user(user_uid: uuid.UUID, data: schemas.UserResponse):
    user = await crud.get_user_by_uid(user_uid)
    await user.update(data)
    return Response(status_code=status.HTTP_200_OK)
