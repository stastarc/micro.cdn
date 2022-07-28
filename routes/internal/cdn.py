from fastapi.routing import APIRouter
from fastapi import UploadFile, File, Form
from fastapi.responses import Response, FileResponse
from database import Content, scope

router = APIRouter(prefix='/cdn')

@router.get("/data/{access_id}")
async def data(access_id: str):
    def status(code: int):
        return status(code)

    if not Content.valid(access_id):
        return status(400)

    path = Content.path(access_id)
    
    if path == None:
        return status(404)
    
    with scope() as sess:
        content = sess.query(Content).filter(Content.access == access_id).first()
        if not content:
            return status(404)
        
        content_type = content.media_type
    
    return FileResponse(path, media_type=content_type)
    

@router.post("/upload")
async def upload(
        file: UploadFile = File(),
        detail: str = Form(max_length=200),
        level: int | str = Form(default=0),
    ):
    def status(code: int):
        return Response(status_code=code)

    with scope() as sess:
        access = Content.register(
            sess=sess,
            file=file,
            detail=detail,
            level=level,
        )

        if access == None:
            return status(404)

        Content.file_save(access, file)
        sess.commit()

    return Response(access)


@router.post("/delete")
async def delete(
        access: str = Form(max_length=32),
    ):
    def status(code: int):
        return Response(status_code=code)

    if not Content.valid(access):
        return status(400)

    if Content.file_delete(access) == None:
        return status(404)

    with scope() as sess:
        content = sess.query(Content).filter(Content.access == access).first()
        if not content:
            return status(404)

        sess.delete(content)
        Content.file_delete(access)
        sess.commit()

    return status(200)