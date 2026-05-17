import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from schemas import Photo, PhotoCreate

app = FastAPI(title="Photos Microservice")

photos_db: List[Photo] = []
id_counter = 1


@app.post("/photos/", response_model=Photo, status_code=status.HTTP_201_CREATED)
async def create_photo(photo: PhotoCreate):
    global id_counter
    new_photo = Photo(
        id=id_counter,
        name=photo.name,
        url=photo.url,
        created_at=datetime.now()
    )
    photos_db.append(new_photo)
    id_counter += 1
    return new_photo


@app.get("/photos/", response_model=List[Photo])
async def get_photos():
    return photos_db


@app.get("/health")
async def health_check():
    return {"status": "ok"}