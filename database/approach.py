
from datetime import datetime
import random
import string
from typing import Any
from . import db

TABLE = 'approach'
KEY_CHARACTERS = string.ascii_lowercase + string.ascii_uppercase + string.digits
KEY_LENGTH = 32

READ = 0
WRITE = 1
DELETE = 2
MANAGE = 3

def exists(key: str):
    return next(iter(db.fetchone(f'select exists (select id from `{TABLE}` where `key`=%s)', (key,)).values())) == 1
    
def details(key: str, col: str = '*', check_exp: bool = True) -> dict[str, Any] | None:
    return db.fetchone(
        f'select {col} from `{TABLE}` where `key`=%s {"and exp is null or exp > current_timestamp" if check_exp else ""}',
        (key,)
    )

def detail(key: str, col: str, default: Any = None, check_exp: bool = True):
    d = details(key, col, check_exp=check_exp)
    return d[col] if d else default

def list(offset: int, count: int, role: int, level: int) -> list[dict[str, Any]]:
    return db.fetchall(f'select * from `{TABLE}` where `role`<%s and `level`<=%s limit %s, %s',
        (role, level, offset, count))

def is_accessible(key: str, level: int = 0, check_exp: bool = True) -> bool | None:
    if level <= 255:
        return detail(key, 'level', default=-1, check_exp=check_exp) >= level
    else:
        d = details(key, 'id,level', check_exp=check_exp)
        if d == None: return None
        return d['id'] == level - 255 or d['level'] > 1

def create_key() -> str:
    key = ''.join(random.choice(KEY_CHARACTERS) for _ in range(KEY_LENGTH))
    
    if exists(key):
        return create_key()

    return key

def create(level: int = 0, tag: str | None = None, role: int = READ, exp: datetime | None = None) -> str:
    key = create_key()
    db.execute(f'insert into `{TABLE}` (`key`,`level`,`tag`,`role`,`exp`) values (%s,%s,%s,%s,%s)',
        (key, level, tag, role, exp))

    return key

def delete(key: str) -> bool:
    return db.execute(f'delete from `{TABLE}` where `key`=%s', (key,)) == 1