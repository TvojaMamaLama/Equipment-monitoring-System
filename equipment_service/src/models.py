import uuid
from enum import Enum
from typing import Optional

import ormar
import sqlalchemy
import databases

from settings import DATABASE_URL

metadata = sqlalchemy.MetaData()
database = databases.Database(DATABASE_URL)


class MainMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Statuses(Enum):
    activate = "ACTIVATE"
    deactivate = "DEACTIVATE"
    discard = "DISCARD"


class EquipmentModel(ormar.Model):
    uid: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    name: str = ormar.String(max_length=50, unique=True)

    class Meta(MainMeta):
        tablename = "equipment_model"


class Equipment(ormar.Model):
    uid: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    name: str = ormar.String(unique=True, max_length=50)
    model: Optional[EquipmentModel] = ormar.ForeignKey(EquipmentModel)
    status: str = ormar.String(max_length=15, choices=list(Statuses), default=Statuses.activate.value)

    class Meta(MainMeta):
        tablename = "equipment"
