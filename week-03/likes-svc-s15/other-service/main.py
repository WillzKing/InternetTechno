from fastapi import FastAPI
from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Other Service")

class Item(BaseModel):
    id: int
    name: str
    created_at: datetime

items_db: List[Item] = []
id_counter = 1


@app.post("/other/", response_model=Item, status_code=201)
async def create_item(name: str):
    global id_counter
    new_item = Item(
        id=id_counter,
        name=name,
        created_at=datetime.now()
    )
    items_db.append(new_item)
    id_counter += 1
    return new_item


@app.get("/other/", response_model=List[Item])
async def get_items():
    return items_db


@app.get("/other/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = next((i for i in items_db if i.id == item_id), None)
    if not item:
        return {"error": "Item not found"}
    return item


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "other-service"}