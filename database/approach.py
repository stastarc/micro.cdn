# 없애면 안돼ㅑ요~
from .db import engine, factory, scope, Base
import random
import string

from sqlalchemy import Column, exists
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, TINYINT, DATETIME


KEY_CHARACTERS = string.ascii_lowercase + string.ascii_uppercase + string.digits
KEY_LENGTH = 32

class Approach(Base):
    READ = 0
    WRITE = 1
    DELETE = 2
    MANAGE = 3
    
    __tablename__ = 'approach'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    key = Column(VARCHAR(32), primary_key=True)
    level = Column(TINYINT, nullable=False)
    tag = Column(VARCHAR(100), nullable=True)
    exp = Column(DATETIME, nullable=True)
    role = Column(TINYINT, nullable=False)

    @staticmethod
    def exists_key(sess, key) -> bool:
        return sess.query(exists().where(Approach.key == key)).scalar()

    @staticmethod
    def create_key(sess) -> str: # idk session type :(
        while True:
            key = ''.join(random.choice(KEY_CHARACTERS) for _ in range(KEY_LENGTH))

            if not Approach.exists_key(sess, key):
                return key
    
    @staticmethod   
    def get_id(sess, key) -> int | None:
        return sess.query(Approach.id).filter(Approach.key == key).scalar()

    @staticmethod
    def valid(key: str | None) -> bool:
        return key != None and len(key) == 32
        