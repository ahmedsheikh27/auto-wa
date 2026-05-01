from app.models.tables import Order
from sqlalchemy import select

def create_order(db, product_name, product_id, customer_phone, address, status="pending"):

    order = Order(
        product_name=product_name,
        product_id=product_id,
        customer_phone=customer_phone,
        address=address,
        status=status
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return order

def get_orders(db):
    stmt = select(Order)
    result = db.execute(stmt)
    orders = result.scalars.all()
    return orders