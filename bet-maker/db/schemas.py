import enum
import decimal
import time
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: str
    time: int

class User_bet(BaseModel):

users: dict[str, User] = {'ivan': User(id='1', bet=5000, event_id='3', time=int(time.time())),
                          'dima': User(id='2', bet=400, event_id='1', time=int(time.time()) + 90),
                          'user111': User(id='3', bet=1200, event_id='2', time=int(time.time()) - 90)}

