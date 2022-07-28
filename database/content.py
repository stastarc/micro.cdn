from os import mkdir
import os
from os.path import join as path_join, exists as path_exists
import random
import shutil
import string
from typing import Any
from fastapi import UploadFile, File

from env import Env
from . import db

TABLE = 'contents'
IMAGE_ID = str | int
ACCESS_CHARACTERS = string.ascii_lowercase + string.ascii_uppercase + string.digits
ACCESS_LENGTH = 32
CDN_DIR = Env.CDN_DIR

_ = path_exists(CDN_DIR) or mkdir(CDN_DIR)

def __id_column(id: IMAGE_ID) -> str:
    if isinstance(id, str): return 'access'
    if isinstance(id, int): return 'id'
    raise TypeError(f'id must be str or int, not {type(id)}')

def exists(id: IMAGE_ID, level: int | None = 0) -> bool:
    return next(iter(db.fetchone(
        f'select exists (select id from `{TABLE}` where `{__id_column(id)}`=%s{" and level<=%s" if level else ""})',
            (id, level) if level else (id,)).values())) == 1

def details(id: IMAGE_ID, col: str = '*', level: int | None = 0) -> dict[str, Any] | None:
    return db.fetchone(
        f'select {col} from `{TABLE}` where `{__id_column(id)}`=%s{" and level<=%s" if level else ""}',
            (id, level) if level else (id,))

def detail(key: IMAGE_ID, col: str, default: Any = None, level: int | None = 0):
    d = details(key, col, level=level)
    return d[col] if d else default

def list(offset: int, count: int, level: int | None = 0) -> list[dict[str, Any]]:
    return db.fetchall(f'select * from `{TABLE}`{" where level<=%s" + (" or level>=255" if level > 1 else "") if level else ""} limit %s, %s',
        (level, offset, count) if level else (offset, count))

def create_access() -> str:
    access = ''.join(random.choice(ACCESS_CHARACTERS) for _ in range(ACCESS_LENGTH))

    if exists(access, level=None):
        return create_access()

    return access

def register(level: int = 0, title: str | None = None, detail: str | None = None, file: UploadFile = File()) -> str:
    access = create_access()

    db.execute(f'insert into `{TABLE}` (`access`, `level`, `title`, `detail`, `media_type`) values (%s, %s, %s, %s, %s)',
        (access, level, title, detail, file.content_type))
    
    with open(image_path(access), 'wb') as f:
        shutil.copyfileobj(file.file, f)

    return access

def delete(id: IMAGE_ID) -> bool:
    if isinstance(id, int):
        file = detail(id, 'access', level=None)
        if not file: return False
    else:
        file = id

    succ = db.execute(f'delete from `{TABLE}` where `{__id_column(id)}`=%s', (id,)) == 1
    
    if succ:
        path = image_path(file)

        if path_exists(path):
            os.remove(path)

    return succ

def image_path(access_id) -> str:
    return path_join(CDN_DIR, access_id)