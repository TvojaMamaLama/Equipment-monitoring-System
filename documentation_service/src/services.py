import uuid

from pathlib import Path
import aiofiles
from typing import IO, Generator

from fastapi import UploadFile, HTTPException, Request
import ormar

from models import Document


async def save_doc(file: UploadFile):
    file_name = f"docs/{file.filename}"
    if file.content_type == "application/pdf":
        await write_doc(file_name, file)
    else:
        raise HTTPException(status_code=400, detail="It isn't pdf")
    return {"file_name": file_name}


async def write_doc(file_name: str, file: UploadFile):
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        await buffer.write(data)


def ranged(
    file: IO[bytes],
    start: int = 0,
    end: int = None,
    block_size: int = 8192,
) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, "close"):
        file.close()


async def open_doc(request: Request, uid: uuid.UUID) -> tuple:
    try:
        document = await Document.objects.get(file_uid=uid)
    except ormar.exceptions.NoMatch:
        raise HTTPException(status_code=404, detail="Not found")
    path = Path(document.dict().get("content"))
    file = path.open("rb")
    file_size = path.stat().st_size

    content_length = file_size
    status_code = 200
    headers = {}
    # content_range = request.headers.get("range")

    # if content_range is not None:
    #     content_range = content_range.strip().lower()
    #     content_ranges = content_range.split("=")[-1]
    #     range_start, range_end, *_ = map(str.strip, (content_ranges + "-").split("-"))
    #     range_start = max(0, int(range_start)) if range_start else 0
    #     range_end = min(file_size - 1, int(range_end)) if range_end else file_size - 1
    #     content_length = (range_end - range_start) + 1
    #     file = ranged(file, start=range_start, end=range_end + 1)
    #     status_code = 206
    #     headers["Content-Range"] = f"bytes {range_start}-{range_end}/{file_size}"
    file = document.dict().get("content")
    return file, status_code, content_length, headers
