import json
from fastapi.routing import APIRouter
from fastapi import UploadFile, File, Form
from fastapi.responses import Response, StreamingResponse
from database import approach, content

router = APIRouter(prefix="/cdn")

@router.post("/upload")
async def upload(
        file: UploadFile = File(),
        key: str = Form(max_length=32),
        title: str = Form(max_length=500),
        detail: str = Form(max_length=100),
        level: int | str = Form(default=0),
    ):

    if not key or len(key) != 32:
        return Response(status_code=401)
    
    info = approach.details(key, 'role,level')

    if info == None:
        return Response(status_code=401)

    if info['role'] < approach.WRITE:
        return Response(status_code=403)

    if isinstance(level, str):
        level = approach.detail(level, 'id')
        if level == None:
            return Response(status_code=403)
        else: level = int(level) + 255
    elif info['level'] < level:
        return Response(status_code=403)

    access = content.register(
        level=level,
        title=title,
        detail=detail,
        file=file,
    )

    return Response(access)

@router.post("/delete")
async def delete(
        key: str = Form(max_length=32),
        access: str = Form(max_length=32),
    ):

    if not key or len(key) != 32 or not access or len(access) != 32:
        return Response(status_code=401)

    info = approach.details(key, 'role,level')

    if info == None:
        return Response(status_code=401)

    if info['role'] < approach.DELETE:
        return Response(status_code=403)

    level = content.detail(access, 'level', level=None, default=None) 

    if level == None:
        return Response(status_code=404)

    if info['level'] > 1 if level > 255 else info['level'] < level:
        return Response(status_code=403)

    return Response(status_code=200 if content.delete(access) else 404)

@router.post("/list")
async def list(
        key: str = Form(max_length=32),
        offset: int = Form(default=0),
        limit: int = Form(default=10),
    ):

    if not key or len(key) != 32:
        return Response(status_code=401)

    info = approach.details(key, 'role,level')

    if info == None:
        return Response(status_code=401)

    if info['role'] < approach.MANAGE:
        return Response(status_code=403)

    level = info['level']

    def listing():
        yield '{"content":[\n'
        for c in content.list(offset, limit, level=None):
            res = {
                'id': c['id'],
                'access': c['access'],
                'level': c['level'],
                'uploaded_at': c['uploaded_at'].isoformat(),
            }

            accessible = level >= c['level'] or (c['level'] > 255 and level > 1)
            res['accessible'] = accessible

            if accessible:
                res['title'] = c['title']
                res['detail'] = c['detail']
                res['media_type'] = c['media_type']

            yield json.dumps(res, separators=(',', ':'))
            yield ',\n'
        yield ']}'

    return StreamingResponse(listing(), media_type='text/plain')

