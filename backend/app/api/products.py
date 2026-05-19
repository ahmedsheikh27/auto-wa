from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.product_service import search_products, get_all_products

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
async def list_products(db: Session = Depends(get_db)):
    return await get_all_products(db)


@router.get("/search")
async def search(db: Session = Depends(get_db), query: str = ""):
    return await search_products(db, query)


# @router.get("/{slug}")
# async def get_product(query: str):
#     return await get_product_by_slug(query)
