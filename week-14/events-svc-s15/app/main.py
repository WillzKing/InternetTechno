import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from schemas import Event, EventCreate

app = FastAPI(title="Events Microservice")

events_db: List[Event] = []
id_counter = 1


@app.post("/events/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate):
    global id_counter
    new_event = Event(
        id=id_counter,
        name=event.name,
        location=event.location,
        created_at=datetime.now()
    )
    events_db.append(new_event)
    id_counter += 1
    return new_event


@app.get("/events/", response_model=List[Event])
async def get_events():
    return events_db


@app.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: int):
    event = next((e for e in events_db if e.id == event_id), None)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Событие с ID {event_id} не найдено"
        )
    return event


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "events-svc-s15"}