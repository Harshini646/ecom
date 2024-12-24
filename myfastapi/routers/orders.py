from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..services import OrderService
from ..database import get_db
from ..schemas import Order

router = APIRouter()

@router.get("/orders", response_model=list[Order])
def get_all_orders(db: Session = Depends(get_db)):
    return OrderService.get_all_orders()

@router.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    return OrderService.get_order(order_id)

@router.post("/orders/{user_id}", response_model=Order)
def create_order(user_id: int, db: Session = Depends(get_db)):
    return OrderService.create_order(user_id)

@router.delete("/orders/{order_id}", response_model=dict)
def remove_order(order_id: int, db: Session = Depends(get_db)):
    return OrderService.remove_order(order_id)
