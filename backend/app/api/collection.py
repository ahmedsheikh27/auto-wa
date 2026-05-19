from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.product_service import get_all_collections, get_collection_products

router = APIRouter(prefix="/collection", tags=["Collection"])


@router.get("/")
async def list_collections(db: Session = Depends(get_db)):
    return await get_all_collections(db)


@router.get("/{slug}")
async def collection_products(slug: str, db: Session = Depends(get_db)):
    return await get_collection_products(db, slug)
