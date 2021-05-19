import uuid

from fastapi import FastAPI, Response, status, Path, Body

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


@app.get("/equipment")
async def get_list():
    equipments = await Equipment.objects.select_related("model").exclude_fields(["model__equipments"]).all()
    return equipments


@app.post("/equipment")
async def create(equipment: Equipment):
    await equipment.save()
    return equipment


@app.put("/equipment/{uid}")
async def update(uid: uuid.UUID = Path(...), equipment: Equipment = Body(...)):
    equipment_db = await Equipment.objects.get_or_none(uid=uid)
    if not equipment_db:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    equipment_db = await equipment_db.update(**equipment.dict(exclude={"uid"}))
    return equipment_db


@app.patch("/equipment/{uid}")
async def partial_update(uid: uuid.UUID = Path(...), equipment: Equipment = Body(...)):
    equipment_db = await Equipment.objects.get_or_none(uid=uid)
    if not equipment_db:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await equipment_db.update(**equipment.dict(exclude={"uid"}))
    return equipment_db


@app.delete("/equipment/{uid}")
async def delete(uid: uuid.UUID):
    eq = await Equipment.objects.delete(uid=uid)
    if not eq:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/equipment-model")
async def get_list():
    equipment_models = await EquipmentModel.objects.all()
    return equipment_models


@app.post("/equipment-model")
async def create(eq_model: EquipmentModel):
    eq_model = await EquipmentModel.objects.create(**eq_model.dict())
    return eq_model


@app.patch("/equipment-model/{uid}")
async def partial_update(uid: uuid.UUID = Path(...), eq_model: EquipmentModel = Body(...)):
    equipment_model_db = await Equipment.objects.get_or_none(uid=uid)
    if not equipment_model_db:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    await equipment_model_db.update(**eq_model.dict(exclude={"uid"}))
    return equipment_model_db
