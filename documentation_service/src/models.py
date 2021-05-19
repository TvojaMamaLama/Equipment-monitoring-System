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


class Document(ormar.Model):
    class Meta(MainMeta):
        tablename = "documents"

    file_uid: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    file_name: str = ormar.String(max_length=50, unique=True)
    content: str = ormar.String(max_length=1000)
    equipment_model_uid: uuid.UUID = ormar.UUID()
