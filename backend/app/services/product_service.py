from sqlalchemy import select
from app.models.tables import Product, Collection


async def search_products(db, query: str):
    stmt = select(Product).where(Product.title.ilike(f"%{query}%"))
    result = db.execute(stmt)
    products = result.scalars().all()
    return products


async def get_all_products(db):
    return db.query(Product).all()

async def get_product_by_id(db, id: int):
    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        return {
            "product": []
        }

    return {
        "product": {
            "id": product.id,
            "title": product.title,
            "description": product.description,
        }
    }

async def search_collection_products(db, query: str):
    stmt = select(Collection).where(Collection.title.ilike(f"%{query}%"))
    result = db.execute(stmt)
    collections = result.scalars().all()
    return collections


async def get_all_collections(db):
    return db.query(Collection).all()


async def get_collection_products(db, slug: str):
    collection = db.query(Collection).filter(Collection.slug == slug).first()

    if not collection:
        return {
            "collection": None,
            "products": []
        }

    return {
        "collection": {
            "id": collection.id,
            "title": collection.title,
            "description": collection.description,
            "slug": collection.slug
        },
        "products": collection.products
    }