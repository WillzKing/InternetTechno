import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from schemas import Session, SessionCreate

app = FastAPI(title="Sessions Microservice")

sessions_db: List[Session] = []
id_counter = 1


@app.post("/sessions/", response_model=Session, status_code=status.HTTP_201_CREATED)
async def create_session(session: SessionCreate):
    global id_counter
    new_session = Session(
        id=id_counter,
        name=session.name,
        ip=session.ip,
        created_at=datetime.now()
    )
    sessions_db.append(new_session)
    id_counter += 1
    return new_session


@app.get("/sessions/", response_model=List[Session])
async def get_sessions():
    return sessions_db


@app.get("/sessions/{session_id}", response_model=Session)
async def get_session(session_id: int):
    session = next((s for s in sessions_db if s.id == session_id), None)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сессия с ID {session_id} не найдена"
        )
    return session


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "sessions-svc-s15"}