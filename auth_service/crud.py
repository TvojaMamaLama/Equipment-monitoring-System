from sqlalchemy.orm import Session

import models
import schemas
import auth


def get_user_by_uid(db: Session, user_uid: int):
    return db.query(models.User).filter(models.User.id == user_uid).first()


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_user_by_login(db: Session, user_login):
    return db.query(models.User).filter(models.User.login == user_login).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(login=user.login, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
