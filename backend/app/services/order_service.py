from app.models.tables import Order, OrderItem, User
from sqlalchemy import select

def create_order(db, user_id: int, items: list, address: str, status="pending"):
    """
    Create order with multiple items
    items: [{"product_id": 1, "quantity": 2}, ...]
    """
    
    order = Order(
        user_id=user_id,
        status=status,
        address=address
    )
    db.add(order)
    db.flush()  
    
    # Add items to order
    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item["product_id"],
            quantity=item.get("quantity", 1)
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(order)
    return order

def get_orders_by_phone(db, phone: str):
    """Get all orders for a user by phone number"""
    stmt = select(User).where(User.user_phone == phone)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        return print(f'No oders found with this phone number: {phone}')
    
    stmt = select(Order).where(Order.user_id == user.id)
    result = db.execute(stmt)
    orders = result.scalars().all()
    return orders

def get_order_by_id(db, order_id: int):
    """Get order by ID with all items"""
    stmt = select(Order).where(Order.id == order_id)
    result = db.execute(stmt)
    order = result.scalar_one_or_none()
    return order

def update_order_status(db, order_id: int, status: str):
    stmt = select(Order).where(Order.id == order_id)
    result = db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        return None
    order.status = status
    db.commit()
    db.refresh(order)
    return order