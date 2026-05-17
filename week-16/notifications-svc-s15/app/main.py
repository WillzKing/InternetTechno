import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from schemas import Notification, NotificationCreate

app = FastAPI(title="Notifications Microservice")

notifications_db: List[Notification] = []
id_counter = 1


@app.post("/notifications/", response_model=Notification, status_code=status.HTTP_201_CREATED)
async def create_notification(notification: NotificationCreate):
    global id_counter
    new_notification = Notification(
        id=id_counter,
        name=notification.name,
        channel=notification.channel,
        created_at=datetime.now()
    )
    notifications_db.append(new_notification)
    id_counter += 1
    return new_notification


@app.get("/notifications/", response_model=List[Notification])
async def get_notifications():
    return notifications_db


@app.get("/notifications/{notification_id}", response_model=Notification)
async def get_notification(notification_id: int):
    notification = next((n for n in notifications_db if n.id == notification_id), None)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Уведомление с ID {notification_id} не найдено"
        )
    return notification


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "notifications-svc-s15"}