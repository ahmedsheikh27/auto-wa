from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.product_service import get_all_products, search_products

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return get_all_products(db)

@router.get("/search")
def search(q: str, db: Session = Depends(get_db)):
    return search_products(db, q)