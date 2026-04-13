from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderBase(BaseModel):
    name: str
    priority: int

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    name: Optional[str] = None
    priority: Optional[int] = None

class Order(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True