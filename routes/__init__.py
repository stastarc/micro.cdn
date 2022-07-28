from fastapi import FastAPI
from . import get, cdn, manage, internal

def include(app: FastAPI):
    app.include_router(get.router)
    app.include_router(cdn.router)
    app.include_router(manage.router)
    app.include_router(internal.router)