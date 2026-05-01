from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.order_service import get_orders, create_order

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/")
def list_orders(db: Session = Depends(get_db)):
    return get_orders(db)

@router.post("/")
def create(data: dict, db: Session = Depends(get_db)):
    return create_order(db, data["phone"], data["product"], data["address"])