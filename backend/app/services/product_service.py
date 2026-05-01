from sqlalchemy import select
from app.models.tables import Product

def search_products(db, query: str):
    stmt = select(Product).where(Product.name.ilike(f"%{query}%"))
    result = db.execute(stmt)
    products = result.scalars().all()

    return products

def get_all_products(db):
    stmt = select(Product)
    result = db.execute(stmt)
    products = result.scalars.all()
    return products