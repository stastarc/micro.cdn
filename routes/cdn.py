from fastapi.routing import APIRouter
from fastapi import UploadFile, File, Form
from fastapi.responses import Response
from database import Approach, Content, scope

router = APIRouter(prefix="/cdn")

@router.post("/upload")
async def upload(
        file: UploadFile = File(),
        key: str = Form(max_length=32),
        detail: str = Form(max_length=200),
        level: int | str = Form(default=0),
    ):
    def status(code: int):
        return Response(status_code=code)

    if Approach.valid(key): return status(400)
    
    with scope() as sess:
        approach = sess.query(Approach).filter(Approach.key == key).first()

        if approach == None: return status(401)
        
        if isinstance(level, int):
            alevel = approach.level
            if alevel < Approach.WRITE or alevel < level:
                return status(403)

        access = Content.register(
            sess=sess,
            file=file,
            level=level,
            detail=detail,
        )

        if access == None: return status(404)

        Content.file_save(access, file)

        sess.commit()

    return Response(access)

@router.post("/delete")
async def delete(
        key: str = Form(max_length=32),
        access: str = Form(max_length=32),
    ):
    def status(code: int):
        return Response(status_code=code)

    if not Approach.valid(key) or not Content.valid(access):
        return status(400)
        

    with scope() as sess:
        approach = sess.query(Approach).filter(Approach.key == key).first()

        if approach == None: return status(401)
        if approach.role < Approach.DELETE: return status(403)

        alevel = approach.level
        content = sess.query(Content).filter(Content.access == access).first()

        if content == None: return status(404)

        level = content.level

        if alevel < Approach.DELETE or (alevel < 2 if level > 255 else alevel < level):
            return status(403)

        sess.delete(content)
        sess.commit()

    Content.file_delete(access)

    return status(200)
