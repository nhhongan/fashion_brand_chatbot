from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.Order import Order  # Adjust the path to where your Order model is defined

from database.session import get_db  # Replace with your actual DB session dependency
from fastapi import APIRouter

router = APIRouter(
    prefix="/order",
    tags=["order"]
)


@router.get("/")
def get_all_orders(db: Session = Depends(get_db)):
    """
    Retrieve all orders from the database.
    """
    orders = db.query(Order).all()
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders