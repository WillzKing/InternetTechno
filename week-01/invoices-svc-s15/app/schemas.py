from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InvoiceBase(BaseModel):
    name: str
    amount: float

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True