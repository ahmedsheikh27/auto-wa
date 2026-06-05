from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.sdk import create_sdk

router = APIRouter(prefix="/collection", tags=["Collection"])


@router.get("/")
def list_collections(db: Session = Depends(get_db)):
    return create_sdk(db).collections.list()


@router.get("/{slug}")
def collection_products(slug: str, db: Session = Depends(get_db)):
    collection = create_sdk(db).collections.get_products(slug)
    if not collection:
        return {"collection": None, "products": []}
    return collection
