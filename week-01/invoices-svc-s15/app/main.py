from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from app.schemas import Invoice, InvoiceCreate

app = FastAPI(title="Invoices Microservice")

invoices_db: List[Invoice] = []
id_counter = 1


@app.post("/invoices/", response_model=Invoice, status_code=status.HTTP_201_CREATED)
async def create_invoice(invoice: InvoiceCreate):
    global id_counter
    new_invoice = Invoice(
        id=id_counter,
        name=invoice.name,
        amount=invoice.amount,
        created_at=datetime.now()
    )
    invoices_db.append(new_invoice)
    id_counter += 1
    return new_invoice


@app.get("/invoices/", response_model=List[Invoice])
async def get_invoices():
    return invoices_db


@app.get("/invoices/{invoice_id}", response_model=Invoice)
async def get_invoice(invoice_id: int):
    invoice = next((i for i in invoices_db if i.id == invoice_id), None)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Инвойс с ID {invoice_id} не найден"
        )
    return invoice


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "invoices-svc-s15"}