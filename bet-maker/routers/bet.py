import asyncio

from fastapi import Path, FastAPI, HTTPException, APIRouter
from models.models import User, users
import aio_pika
import time
import re


lst = []
my_dict = {}
queue_name = "ch_line"

def format(lst):
    strings = str(lst).split('Event(')[1:]
    j = 0

    for item in strings:
        item = item.strip().rstrip(", ").split(", ")
        temp_dict = {}
        for i in item:
            if '=' in i:
                key, value = i.split("=")
                temp_dict[key] = value
                if len(temp_dict) == 4:
                    j += 1
                    my_dict[str(j)] = temp_dict
    return my_dict

async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    global lst
    async with message.process():
        lst.clear()
        lst.append(message.body)
        await asyncio.sleep(1)

router = APIRouter()

@router.get('/connect')
async def connect():
    global queue_name

    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=100)
    queue = await channel.declare_queue(queue_name, auto_delete=True)

    await queue.consume(process_message)
    try:
        await asyncio.Future()
    finally:
        await connection.close()

@router.get('/events')
async def get_events():
    global my_dict

    my_dict.clear()
    my_dict = format(lst)
    print(my_dict)

    return my_dict

@router.post('/create_user_rate')
async def create_user_rate(user: User):
    if user.name not in users:
        users[user.name] = user
        return 'Append new user'

    else:
        return 'The user name of the account has already been created'

@router.post('/bet')
async def put_bet(name: str):
    try:
        if name in users and my_dict is not None:
            if my_dict[users[name].event_id]:
                if int(users[name].time) > int(my_dict[users[name].event_id]['deadline']):
                    return 'The your bet in activate'
                else:
                    return 'time bet is up'
        else:
            return 'Error'

    except KeyError:
        return 'Error: not found bet'

@router.get('/bet_info/{bet_id}')
async def get_info_bet(name: str, id_event: str):
    if name in users:
        print(time.time())
        print(users[name].time)

        print(int(my_dict[id_event]['deadline']))
        if int(time.time()) > int(my_dict[id_event]['deadline']):
            return f'Your winnings are users[name].bet * {my_dict[id_event]["coefficient"]}'
        else:
            return 'Your bet is not time up'
    else:
        return 'User not found'

