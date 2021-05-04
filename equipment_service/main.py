from fastapi import FastAPI

import schemas
from models import database, EquipmentModel, Equipment


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


@app.post("/equipment", response_model=schemas.EquipmentResponse)
async def create(equipment: schemas.EquipmentCreate):
    equipment = await Equipment.objects.create(equipment)
    return equipment


@app.post("/equipment-model")
async def create(eq_model: schemas.EquipmentModelCreate):
    eq_model = await EquipmentModel.objects.create(**eq_model.dict())
    return eq_model
