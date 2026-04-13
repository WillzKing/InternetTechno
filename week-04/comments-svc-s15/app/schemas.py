import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class CommentStatus(str, Enum):
    NEW = "NEW"
    PAID = "PAID"
    DONE = "DONE"
    CANCELLED = "CANCELLED"

class CommentBase(BaseModel):
    name: str
    author: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    created_at: datetime
    status: CommentStatus = CommentStatus.NEW

    class Config:
        from_attributes = True