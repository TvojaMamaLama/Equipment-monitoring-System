import os.path
import uuid

from fastapi import (
    FastAPI,
    File,
    UploadFile,
    HTTPException,
    Request,
    status,
    Path,
    Body,
    Response,
    Depends
)
from fastapi.responses import FileResponse

from models import database, Document
from services import save_doc, open_doc
from auth import HTTPHeaderAuthentication


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


@app.get("/document")
async def document_list():
    return await Document.objects.all()


@app.post("/document")
async def create_document(document: Document, _: uuid.UUID = Depends(HTTPHeaderAuthentication(scopes=["admin"]))):
    if os.path.isfile(document.content):
        return await Document.objects.create(**document.dict())
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="file with this content not exist, save file first")


@app.put("/document/{uid}")
async def update_document(uid: uuid.UUID = Path(...), document: Document = Body(...), _: uuid.UUID = Depends(HTTPHeaderAuthentication(scopes=["admin"]))):
    if os.path.isfile(document.content):
        document = Document(uid=uid, **document.dict(exclude={"uid"}))
        return await document.upsert()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="file with this content not exist, save file first")


@app.patch("/document/{uid}")
async def partial_update_document(uid: uuid.UUID = Path(...), document: Document = Body(...), _: uuid.UUID = Depends(HTTPHeaderAuthentication(scopes=["admin"]))):
    if os.path.isfile(document.content):
        document_db = await Document.objects.get_or_none(uid=uid)
        if not document_db:
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        await document_db.update(**document.dict(exclude={"uid"}))
        return document_db
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="file with this content not exist, save file first")


@app.delete("/document/{uid}")
async def delete(uid: uuid.UUID, _: uuid.UUID = Depends(HTTPHeaderAuthentication(scopes=["admin"]))):
    document = await Document.objects.delete(uid=uid)
    if not document:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/document/file_upload")
async def save_file(file: UploadFile = File(...), _: uuid.UUID = Depends(HTTPHeaderAuthentication(scopes=["admin"]))):
    return await save_doc(file)


@app.get("/document/{uid}/file")
async def get_doc_file(request: Request, uid: uuid.UUID) -> FileResponse:
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
