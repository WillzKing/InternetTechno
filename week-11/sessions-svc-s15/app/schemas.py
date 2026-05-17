import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from pydantic import BaseModel
from datetime import datetime

class SessionBase(BaseModel):
    name: str
    ip: str

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True