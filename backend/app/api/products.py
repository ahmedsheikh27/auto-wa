from fastapi import APIRouter, Depends
from app.services.hygraph_service import (
    get_product_by_slug 
)

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.product_service import  search_products, get_all_products
router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
async def list_products(db: Session = Depends(get_db)):
    result = await get_all_products(db)
    if not result:
        return "No products in database, try different search"
    products = []
    for i, p in enumerate(result, start=1):
        products.append(
            f"{i}. Product Name: { p.title}\n Product Desc:{p.description}\n "
        )
    print(f"List product tool result: {products}")
    return "\n".join(products)


@router.get("/search")
async def search(db: Session = Depends(get_db), query:str = ''):
    return await search_products(db, query)


@router.get("/{slug}")
async def get_product(query: str):
    return await get_product_by_slug(query)