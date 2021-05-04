import uuid
from pydantic import BaseModel
from typing import Optional, List


class EquipmentModel(BaseModel):
    uid: uuid.UUID
    name: str


class EquipmentResponse(BaseModel):
    uid: uuid.UUID
    name: str
    status: str
    model: Optional[EquipmentModel]


class EquipmentModelResponse(EquipmentModel):
    equipments: List[EquipmentResponse]


class EquipmentCreate(BaseModel):
    name: str
    model: Optional[EquipmentModel]
    status: str


class EquipmentModelCreate(BaseModel):
    name: str
