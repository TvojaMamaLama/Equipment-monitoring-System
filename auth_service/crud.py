import uuid

from models import User
from schemas import UserCreate
import auth


async def get_all_users():
    return await User.objects.all()


async def get_user_by_uid(user_uid: uuid.UUID):
    return await User.objects.get(uid=user_uid)


async def get_user_by_login(user_login):
    return await User.objects.get_or_none(login=user_login)


async def create_user(user: UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = User(login=user.login, password=hashed_password)
    await db_user.save()
    return db_user
