from datetime import datetime
from fastapi.routing import APIRouter
from fastapi import Form
from fastapi.responses import Response
from database import Approach, scope

router = APIRouter(prefix="/manage")

@router.post("/create")
async def create(
        key: str = Form(),
        level: int = Form(default=0),
        tag: str | None = Form(default=None, max_length=100),
        exp: datetime | None = Form(default=None),
        role: int = Form(default=0),
    ):
    def status(code: int):
        return Response(status_code=code)

    if not Approach.valid(key):
        return status(400)

    with scope() as sess:
        approach = sess.query(Approach).filter(Approach.key == key).first()

        if approach == None:
            return status(401)

        if approach.level < Approach.MANAGE or approach.level <= level or approach.role <= role:
            return status(403)

        if level < Approach.READ or level > 255 or (exp != None and exp < datetime.now()):
            return status(400)

        new_key = Approach.create_key(sess)

        sess.add(Approach(
            key=new_key,
            level=level,
            tag=tag,
            exp=exp,
            role=role,
        ))

        sess.commit()

    return Response(new_key)

@router.post("/delete")
async def delete(
        key: str = Form(),
        target_key: str = Form(),
    ):
    def status(code: int):
        return Response(status_code=code)

    if not Approach.valid(key) or not Approach.valid(target_key) or key == target_key:
        return status(400)
    
    with scope() as sess:
        approach = sess.query(Approach).filter(Approach.key == key).first()

        if approach == None:
            return status(401)

        target = sess.query(Approach).filter(Approach.key == target_key).first()

        if target == None:
            return status(404)

        if approach.level < Approach.MANAGE or approach.level <= target.level or approach.role <= target.role:
            return status(403)

        sess.delete(target)
        sess.commit()
    
    return status(200)