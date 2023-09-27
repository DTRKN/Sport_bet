import asyncio

from fastapi import Path, FastAPI, HTTPException, APIRouter
from db.schemas import User, users
from libs.data_handling import Data_handling
from config import channel_rb, exchange_rb
import aio_pika
import time
import logging
import collections
import re

data_hand = Data_handling()
router = APIRouter()

async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():

        await data_hand.clear()
        await data_hand.append(message.body)
        await data_hand.format()
        print('Get data from line-prov')

        await asyncio.sleep(1)
@router.get('/connect')
async def connect():
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/",
    )
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=100)
    channel = await connection.channel()

    await channel.declare_exchange(exchange_rb, durable=True)

    queue = await channel.declare_queue(channel_rb, auto_delete=False, durable=True)
    await queue.consume(process_message)

    try:
        await asyncio.Future()
    finally:
        await connection.close()

@router.get('/events')
async def get_events():

    my_dict = await data_hand.get_dict()

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

    my_dict = await data_hand.get_dict()
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

        my_dict = await data_hand.get_dict()

        print(time.time())
        print(int(my_dict[id_event]['deadline']))

        if int(time.time()) > int(my_dict[id_event]['deadline']):
            return f'Your winnings are users[name].bet * {my_dict[id_event]["coefficient"]}'
        else:
            return 'Your bet is not time up'
    else:
        return 'User not found'

