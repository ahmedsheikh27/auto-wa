from app.models.tables import Order, OrderItem, User, Product
from sqlalchemy import select
from datetime import datetime

def create_order(db, user_id: int, items: list, address: str, status="pending"):
    """
    Create order with multiple items
    items: [{"product_id": 1, "quantity": 2}, ...]
    
    Returns: Order object with all details
    """
    
    print(f"create_order called with user_id={user_id}, items={items}, address={address}")
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            print(f"User with ID {user_id} not found")
            return None
        
        for item in items:
            product = db.query(Product).filter(Product.id == item["product_id"]).first()
            if not product:
                print(f"Product with ID {item['product_id']} not found")
                return None
        
        order = Order(
            user_id=user_id,
            status=status,
            address=address,
            created_at=datetime.utcnow()
        )
        db.add(order)
        db.flush()  
        
        print(f"Order created with ID: {order.id}")
        
        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item["product_id"],
                quantity=item.get("quantity", 1)
            )
            db.add(order_item)
            print(f"Added item: product_id={item['product_id']}, quantity={item.get('quantity', 1)}")
        
        db.commit()
        db.refresh(order)
        
        print(f"Order {order.id} committed successfully")
        return order
        
    except Exception as e:
        db.rollback()
        print(f"Error in create_order: {str(e)}")
        raise


def get_orders_by_phone(db, phone: str):
    """Get all orders for a user by phone number"""
    print(f"🔍 get_orders_by_phone called for phone: {phone}")
    
    try:
        stmt = select(User).where(User.user_phone == phone)
        result = db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"No user found with phone: {phone}")
            return []
        
        stmt = select(Order).where(Order.user_id == user.id)
        result = db.execute(stmt)
        orders = result.scalars().all()
        
        print(f"Found {len(orders)} orders for user {user.id}")
        return orders
        
    except Exception as e:
        print(f"Error in get_orders_by_phone: {str(e)}")
        return []


def get_order_by_id(db, order_id: int):
    """Get order by ID with all items"""
    print(f"🔍 get_order_by_id called for order_id: {order_id}")
    
    try:
        stmt = select(Order).where(Order.id == order_id)
        result = db.execute(stmt)
        order = result.scalar_one_or_none()
        
        if not order:
            print(f"Order with ID {order_id} not found")
            return None
        
        print(f"Found order {order_id}")
        return order
        
    except Exception as e:
        print(f"Error in get_order_by_id: {str(e)}")
        return None


def update_order_status(db, order_id: int, status: str):
    """Update order status (pending/confirmed/cancelled/delivered)"""
    print(f"update_order_status called for order_id={order_id}, status={status}")
    
    try:
        stmt = select(Order).where(Order.id == order_id)
        result = db.execute(stmt)
        order = result.scalar_one_or_none()
        
        if not order:
            print(f"Order with ID {order_id} not found")
            return None
        
        order.status = status
        db.commit()
        db.refresh(order)
        
        print(f"Order {order_id} status updated to: {status}")
        return order
        
    except Exception as e:
        db.rollback()
        print(f"Error in update_order_status: {str(e)}")
        raise


def get_order_summary(db, order_id: int):
    """Get order with all items and product details for summary"""
    print(f"get_order_summary called for order_id: {order_id}")
    
    try:
        stmt = select(Order).where(Order.id == order_id)
        result = db.execute(stmt)
        order = result.scalar_one_or_none()
        
        if not order:
            print(f"Order with ID {order_id} not found")
            return None
        
        order_data = {
            "order_id": order.id,
            "user_id": order.user_id,
            "status": order.status,
            "address": order.address,
            "created_at": order.created_at,
            "items": []
        }
        
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                order_data["items"].append({
                    "product_id": item.product_id,
                    "product_name": product.title,
                    "quantity": item.quantity,
                    "description": product.description
                })
        
        print(f"Order summary retrieved: {len(order_data['items'])} items")
        return order_data
        
    except Exception as e:
        print(f"Error in get_order_summary: {str(e)}")
        raise