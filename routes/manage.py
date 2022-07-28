from datetime import datetime
import json
from fastapi.routing import APIRouter
from fastapi import Form
from fastapi.responses import Response, StreamingResponse
from database import approach

router = APIRouter(prefix="/manage")

@router.post("/create")
async def create(
        key: str = Form(),
        level: int = Form(default=0),
        tag: str | None = Form(default=None, max_length=100),
        exp: datetime | None = Form(default=None),
        role: int = Form(default=0),
    ):

    if not key or len(key) != 32:
        return Response(status_code=401)

    key_info = approach.details(key, 'role,level')

    if not key_info or key_info['role'] < approach.MANAGE:
        return Response(status_code=401)

    if role >= key_info['role'] or level > key_info['level']:
        return Response(status_code=403)

    if level < 0 or level > 255 or role < approach.READ or (exp and exp < datetime.now()):
        return Response(status_code=400)

    key = approach.create(
        level=level,
        tag=tag,
        role=role,
        exp=exp
    )

    return Response(key)

@router.post("/delete")
async def delete(
        key: str = Form(),
        target_key: str = Form(),
    ):

    if not key or len(key) != 32 or not target_key or len(target_key) != 32 or key == target_key:
        return Response(status_code=401)
    
    role = approach.detail(key, 'role', None)

    if role == None or role < approach.MANAGE:
        return Response(status_code=401)

    target_role = approach.detail(target_key, 'role', None)

    if target_role == None:
        return Response(status_code=404)

    if role <= target_role:
        return Response(status_code=403)
    
    return Response(status_code=200 if approach.delete(target_key) else 404)


@router.post("/list")
async def list(
        key: str = Form(),
        offset: int = Form(default=0),
        limit: int = Form(default=10),
    ):

    if not key or len(key) != 32:
        return Response(status_code=401)
    
    info = approach.details(key, 'role, level')

    if info == None or info['role'] < approach.MANAGE:
        return Response(status_code=401)
    
    role = info['role']
    level = info['level']

    def listing():
        yield '{"content":[\n'
        for c in approach.list(offset, limit, role=role, level=level):
            yield json.dumps({
                'id': c['id'],
                'key': c['key'],
                'level': c['level'],
                'tag': c['tag'],
                'role': c['role'],
                'exp': c['exp'].isoformat() if c['exp'] else None,
            }, separators=(',', ':'))
            yield ',\n'
        yield ']}'

    return StreamingResponse(listing(), media_type='text/plain')
