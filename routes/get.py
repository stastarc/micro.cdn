from os.path import exists as path_exists
from fastapi.routing import APIRouter
from fastapi.responses import Response, FileResponse
from database import approach, content

router = APIRouter(prefix="/data")

@router.get("/{access_id}")
async def get(access_id: str, key: str | None = None):
    if not access_id or len(access_id) != 32:
        return Response(status_code=400)

    details = content.details(access_id, 'level,media_type')
    file_path = content.image_path(access_id)

    if not details or not path_exists(file_path):
        return Response(status_code=404)

    level = details['level']
    media_type = details['media_type']

    if level != 0 and (not key or not approach.is_accessible(key, level)):
        return Response(status_code=403)

    return FileResponse(file_path, media_type=media_type)
    