from fastapi.routing import APIRouter
from fastapi.responses import Response, FileResponse
from database import Approach, Content, scope

router = APIRouter(prefix="/data")

@router.get("/{access_id}")
async def get(
        access_id: str,
        key: str | None = None
    ):
    def status(code: int):
        return Response(status_code=code)

    path = Content.path(access_id)
    
    if path == None: return status(404)

    with scope() as sess:
        content = sess.query(Content).filter(Content.access == access_id).first()
        if not content: return status(404)

        level = content.level

        if level != 0:
            if not Approach.valid(key): return status(401)

            approach = sess.query(Approach).filter(Approach.key == key).first()

            if approach == None:
                return status(403)

            if level > 255:
                if approach.id != content.level - 255:
                    return status(403)
            elif approach.level < level:
                return status(403)

        
        content_type = content.media_type

    return FileResponse(path, media_type=content_type)
    