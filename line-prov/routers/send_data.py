from models.models import events, Event
from fastapi import Path, FastAPI, HTTPException, APIRouter
import json
import time
import aio_pika

router = APIRouter()
queue_name = "ch_line"
dict_str = [e for e in events.values()]

@router.get('/connect')
async def connect():

    global dict_str, queue_name

    connection = await aio_pika.connect(
        "amqp://guest:guest@127.0.0.1/"
    )
    async with connection:

        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=str(dict_str).encode()),
            routing_key=queue_name,
        )

@router.put('/event')
async def create_event(event: Event):
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



