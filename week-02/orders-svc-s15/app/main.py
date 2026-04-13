from fastapi import FastAPI, HTTPException, status
from typing import List
from datetime import datetime
from schemas import Order, OrderCreate, OrderUpdate

app = FastAPI(title="Orders Microservice")

orders_db: List[Order] = []
id_counter = 1


@app.post("/orders/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    global id_counter
    new_order = Order(
        id=id_counter,
        name=order.name,
        priority=order.priority,
        created_at=datetime.now()
    )
    orders_db.append(new_order)
    id_counter += 1
    return new_order


@app.get("/orders/", response_model=List[Order])
async def get_orders():
    return orders_db


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    order = next((o for o in orders_db if o.id == order_id), None)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заказ с ID {order_id} не найден"
        )
    return order


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order_update: OrderUpdate):
    order = next((o for o in orders_db if o.id == order_id), None)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заказ с ID {order_id} не найден"
        )
    
    if order_update.name is not None:
        order.name = order_update.name
    if order_update.priority is not None:
        order.priority = order_update.priority
    
    return order


@app.delete("/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int):
    global orders_db
    order = next((o for o in orders_db if o.id == order_id), None)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Заказ с ID {order_id} не найден"
        )
    
    orders_db = [o for o in orders_db if o.id != order_id]
    return None


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "orders-svc-s15"}