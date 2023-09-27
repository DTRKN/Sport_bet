from db.schemas import events, Event
from fastapi import Path, FastAPI, HTTPException, APIRouter
import json
import time
from config import channel_rb, exchange_rb
import asyncio
import aio_pika

router = APIRouter()

new_dict_str = None
@router.get('/connect')
async def connect():
    global new_dict_str

    while True:

        await asyncio.sleep(1)

        connection = await aio_pika.connect(
            "amqp://guest:guest@127.0.0.1/"
        )

        dict_str = [e for e in events.values()]

        async with connection:

            channel = await connection.channel()

            await channel.declare_exchange(exchange_rb, durable=True)

            if new_dict_str != dict_str:

                new_dict_str = dict_str
                await channel.default_exchange.publish(
                    aio_pika.Message(body=str(dict_str).encode()),
                    routing_key=channel_rb,
                )

@router.put('/event')
async def create_event(event: Event):
    global events
    if event.event_id not in events:
        events[event.event_id] = event
        return [None]

    for p_name, p_value in event.dict(exclude_unset=True).items():
        setattr(events[event.event_id], p_name, p_value)
    return [None]

@router.get('/event/{event_id}')
async def get_event(event_id: str):
    if event_id in events:
        return events[event_id]

    raise HTTPException(status_code=404, detail='Event not found')

@router.get('/events')
async def get_events():
    return list(e for e in events.values())



