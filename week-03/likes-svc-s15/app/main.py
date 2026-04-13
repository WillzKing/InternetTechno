import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from schemas import Like, LikeCreate

app = FastAPI(title="Likes Microservice")

likes_db: List[Like] = []
id_counter = 1


@app.post("/likes/", response_model=Like, status_code=status.HTTP_201_CREATED)
async def create_like(like: LikeCreate):
    global id_counter
    new_like = Like(
        id=id_counter,
        name=like.name,
        target=like.target,
        created_at=datetime.now()
    )
    likes_db.append(new_like)
    id_counter += 1
    return new_like


@app.get("/likes/", response_model=List[Like])
async def get_likes():
    return likes_db


@app.get("/likes/{like_id}", response_model=Like)
async def get_like(like_id: int):
    like = next((l for l in likes_db if l.id == like_id), None)
    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Лайк с ID {like_id} не найден"
        )
    return like


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "likes-svc-s15"}