from fastapi.routing import APIRouter
from . import cdn

router = APIRouter(prefix='/internal')

router.include_router(cdn.router)