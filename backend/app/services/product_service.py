from sqlalchemy import select
from app.models.tables import Product

async def search_products(db, query: str):
    stmt = select(Product).where(Product.name.ilike(f"%{query}%"))
    result = await db.execute(stmt)
    products = result.scalars().all()

    return products