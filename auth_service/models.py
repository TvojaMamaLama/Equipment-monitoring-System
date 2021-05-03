import uuid

import ormar
import sqlalchemy
import databases

from settings import DATABASE_URL

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    uid: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    login: str = ormar.String(unique=True, max_length=50)
    password = ormar.String(max_length=500)
    is_admin = ormar.Boolean(default=False)

    class Meta(MainMeta):
        tablename = "users"
        order_by = ["-login"]
