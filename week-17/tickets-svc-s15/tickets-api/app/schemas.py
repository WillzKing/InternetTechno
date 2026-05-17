import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from pydantic import BaseModel
from datetime import datetime

class TicketBase(BaseModel):
    name: str
    status: str

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True