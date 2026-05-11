from sqlalchemy import select
from app.models.tables import Product, Collection

async def search_products(db, query: str):
    stmt = select(Product).where(Product.title.ilike(f"%{query}%"))
    result = db.execute(stmt)
    products = result.scalars().all()
    return products

async def get_all_products(db):
    return db.query(Product).all()

async def search_collection_products(db, query: str):
    stmt = ( select(Collection).where(Collection.title.ilike(f"%{query}%")))
    result = db.execute(stmt)
    collections = result.scalars().all()
    return collections

async def get_all_collections(db):
    return db.query(Collection).all()
