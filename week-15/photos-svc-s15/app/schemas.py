import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from pydantic import BaseModel
from datetime import datetime

class PhotoBase(BaseModel):
    name: str
    url: str

class PhotoCreate(PhotoBase):
    pass

class Photo(PhotoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True