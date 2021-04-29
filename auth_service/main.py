from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db import get_db
from crud import get_all_users
import schemas


app = FastAPI()


@app.post("/auth")
def authorization():
    pass


@app.get("/users", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

