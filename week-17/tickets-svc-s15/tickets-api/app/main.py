import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from schemas import Ticket, TicketCreate

app = FastAPI(title="Tickets REST API")

tickets_db: List[Ticket] = []
id_counter = 1


@app.post("/tickets/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketCreate):
    global id_counter
    new_ticket = Ticket(
        id=id_counter,
        name=ticket.name,
        status=ticket.status,
        created_at=datetime.now()
    )
    tickets_db.append(new_ticket)
    id_counter += 1
    return new_ticket


@app.get("/tickets/", response_model=List[Ticket])
async def get_tickets():
    return tickets_db


@app.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: int):
    ticket = next((t for t in tickets_db if t.id == ticket_id), None)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Тикет с ID {ticket_id} не найден"
        )
    return ticket


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "tickets-api"}