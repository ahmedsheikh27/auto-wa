from fastapi import APIRouter, Depends
from app.services.product_service import (
    search_collection_products,
    get_all_collections
)
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter(prefix="/collection", tags=["Colletion"])

@router.get("/")
async def list_products(db:Session = Depends(get_db)):
    result = await get_all_collections(db)
    if not result:
        return "No collection found, try different name or category"
    collections = []
    for i, c in enumerate(result, start=1):
        collections.append(
            f"{i}. collection Name: {c.title}\n Collection Desc:{c.description}\n"
        )
    print(f"List collection tool result: {collections}")

    return "\n".join(collections)



@router.get("/search")
async def search(db:Session = Depends(get_db),query: str = ''):
    collections = await search_collection_products(db, query)

    if not collections:
        return "No collections found 😕"

    responses = []

    for collection in collections:
        col_title = collection.title
        col_products = collection.products

        if not col_products:
            continue

        response = f"{col_title}\n"
        for i, product in enumerate(col_products[:5], start=1):
            response += (
                f"\n{i}. {product.title}\n {product.description}"
            )
        responses.append(response)

    if not responses:
        return "No products found in collections"

    final_response = "\n\n".join(responses)

    print(f"Search collection tool result:\n{final_response}")

    return final_response

   