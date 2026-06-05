from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.sdk import create_sdk

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return create_sdk(db).products.list()


@router.get("/search")
def search(db: Session = Depends(get_db), query: str = ""):
    return create_sdk(db).products.search(query)


# @router.get("/{slug}")
# async def get_product(query: str):
#     return await get_product_by_slug(query)
