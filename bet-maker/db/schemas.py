import enum
import decimal
import time
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: str
    bet: int
    event_id: str

users: dict[str, User] = {'ivan': User(id='1', bet=5000, event_id='3'),
                          'dima': User(id='2', bet=400, event_id='1'),
                          'user111': User(id='3', bet=1200, event_id='2')}

