import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from typing import Dict, List

PROJECT_CODE = "comments-s15"

app = FastAPI(title="WebRTC Signaling Server")

clients: Dict[str, List[WebSocket]] = {"room1": []}


@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    
    if room_id not in clients:
        clients[room_id] = []
    
    clients[room_id].append(websocket)
    print(f"Клиент подключился к комнате {room_id}. Всего клиентов: {len(clients[room_id])}")
    
    try:
        while True:
            data = await websocket.receive_text()
            
            for client in clients[room_id]:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        clients[room_id].remove(websocket)
        print(f"Клиент отключился от комнаты {room_id}. Осталось клиентов: {len(clients[room_id])}")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": PROJECT_CODE}


client_path = os.path.join(os.path.dirname(__file__), "..", "client")
app.mount("/", StaticFiles(directory=client_path, html=True), name="client")