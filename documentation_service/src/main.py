import os.path
import uuid

from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    Request,
    status,
    Response
)
from fastapi.responses import FileResponse

from models import database, Document
from services import save_doc, open_doc


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


@app.post("/document/file_upload")
async def save_file(file: UploadFile = File(...)):
    return await save_doc(file)


@app.get("/document")
async def document_list():
    return await Document.objects.all()


@app.post("/document")
async def create_document(document: Document):
    if os.path.isfile(document.content):
        return await Document.objects.create(**document.dict())
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="file with this content not exist, save file first")


@app.get("/document/{uid}/file")
async def get_streaming_video(request: Request, uid: uuid.UUID) -> FileResponse:
    file, status_code, content_length, headers = await open_doc(request, uid)
    response = FileResponse(
        file,
        media_type="application/pdf",
        status_code=status_code,
    )

    response.headers.update(
        {
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            **headers,
        }
    )
    return response
