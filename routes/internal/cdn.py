from fastapi.routing import APIRouter
from fastapi import UploadFile, File, Form
from fastapi.responses import Response, FileResponse
from database import approach, content
from os.path import exists as path_exists

router = APIRouter(prefix='/cdn')

@router.get("/data/{access_id}")
async def data(access_id: str):
    media_type = content.detail(access_id, 'media_type', level=None)
    file_path = content.image_path(access_id)

    if not id or not path_exists(file_path):
        return Response(status_code=404)

    return FileResponse(file_path, media_type=media_type)
    

@router.post("/upload")
async def upload(
        file: UploadFile = File(),
        title: str = Form(max_length=500),
        detail: str = Form(max_length=100),
        level: int | str = Form(default=0),
    ):

    if isinstance(level, str):
        level = approach.detail(level, 'id')
        if level == None:
            return Response(status_code=403)
        else: level = int(level) + 255

    access = content.register(
        level=level,
        title=title,
        detail=detail,
        file=file,
    )

    return Response(access)


@router.post("/delete")
async def delete(
        access: str = Form(max_length=32),
    ):

    return Response(status_code=200 if content.delete(access) else 404)