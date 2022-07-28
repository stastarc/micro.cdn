# 없애면 안돼ㅑ요~
import os
import shutil
from .db import engine, factory, scope, Base
from .approach import Approach
import random
import string

from sqlalchemy import Column, DateTime, text, exists
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from fastapi import UploadFile
from os import mkdir
from os.path import exists as path_exists, join as path_join
import string

from env import Env

ACCESS_CHARACTERS = string.ascii_lowercase + string.ascii_uppercase + string.digits
ACCESS_LENGTH = 32
CDN_DIR = Env.CDN_DIR

_ = path_exists(CDN_DIR) or mkdir(CDN_DIR)

class Content(Base):
    __tablename__ = 'contents'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    access = Column(VARCHAR(32), primary_key=True)
    level = Column(BIGINT, nullable=False)
    detail = Column(VARCHAR(500), nullable=True)
    media_type = Column(VARCHAR(100), nullable=False)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP()"))

    @staticmethod
    def exists_access(sess, access) -> bool:
        return sess.query(exists().where(Content.access == access)).scalar()

    @staticmethod
    def create_access(sess) -> str: # idk session type :(
        while True:
            access = ''.join(random.choice(ACCESS_CHARACTERS) for _ in range(ACCESS_LENGTH))

            if not Content.exists_access(sess, access):
                return access
        
    @staticmethod
    def register(sess, file: UploadFile, level: int | str, detail: str | None = None) -> str | None:
        if isinstance(level, str):
            id = Approach.get_id(sess, level) 
            if id == None: return None
            level = id + 255

        access = Content.create_access(sess)

        sess.add(Content(
            access=access,
            level=level,
            detail=detail,
            media_type=file.content_type,
        ))

        return access

    @staticmethod
    def file_save(access: str, file: UploadFile):
        path = path_join(CDN_DIR, access)
        
        with open(path, 'wb') as f:
            shutil.copyfileobj(file.file, f)

    @staticmethod
    def file_delete(access: str) -> bool:
        path = Content.path(access)
        if path == None: return False
        os.remove(path)
        return True

    @staticmethod
    def valid(key: str | None) -> bool:
        return key != None and len(key) == 32
    
    @staticmethod
    def path(access: str) -> str | None:
        path = path_join(CDN_DIR, access)

        if not path_exists(path):
            return None
        
        return path