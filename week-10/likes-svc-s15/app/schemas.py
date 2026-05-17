import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from pydantic import BaseModel
from datetime import datetime

class LikeBase(BaseModel):
    name: str
    target: str

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True