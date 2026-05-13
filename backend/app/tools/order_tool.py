from agents import function_tool
from app.db.session import SessionLocal
from app.services.order_service import (
    create_order,
    get_orders_by_phone,
    update_order_status,
    get_order_summary
)
from typing import List
from pydantic import BaseModel

class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int 


@function_tool(
    name_override="create_order_tool",
    description_override=(
        "Create a new order for a user with multiple products. "
        "MUST provide: user_id (integer), items (list of {product_id, quantity}), address (string). "
        "Call this when user confirms order and provides delivery address."
    ),
)
async def create_order_tool(
    user_id: int,
    items: List[OrderItemSchema],
    address: str,
    status: str = "pending",
) -> dict:
    """
    Create a new order for a user with multiple products
    
    Args:
        user_id: The user ID from database
        items: List of order items with product_id and quantity
        address: Delivery address
        status: Order status (default: pending)
    
    Returns:
        Dictionary with success status and order details
    """

    print("create_order_tool")
    print(f"Parameters:")
    print(f"   user_id: {user_id}")
    print(f"   items: {items}")
    print(f"   address: {address}")
    print(f"   status: {status}")

    db = SessionLocal()

    try:
        formatted_items = []
        for item in items:

            new_item = {
                "product_id": item.product_id,
                "quantity": item.quantity,
            }
            formatted_items.append(new_item)

        print(f"Formatted items: {formatted_items}")

        order = create_order(
            db=db,
            user_id=user_id,
            items=formatted_items,
            status=status,
            address=address,
        )

        if not order:
            return {
                "success": False,
                "error": "Order creation failed - user or product not found",
            }
        order_summary = get_order_summary(db, order.id)

        print("order created successfully")

        return {
            "success": True,
            "message": "Order created successfully",
            "order": {
                "order_id": order.id,
                "user_id": order.user_id,
                "status": order.status,
                "address": order.address,
                "items": order_summary["items"],
                "created_at": str(order.created_at),
            },
        }

    except Exception as exc:
        print(f"order creation failed: {str(exc)}")

        return {
            "success": False,
            "error": str(exc),
        }

    finally:
        db.close()


@function_tool(
    name_override="list_orders_by_phone_tool",
    description_override=(
        "Retrieve all orders for a customer using their phone number. "
        "Use this to check order history or track existing orders."
    ),
)
async def list_orders_by_phone_tool(customer_phone: str) -> dict:
    """
    List all orders for a customer by phone number
    
    Args:
        customer_phone: Customer's phone number
    
    Returns:
        Dictionary with success status and list of orders
    """
    
    print("list_orders_by_phone_tool Called")
    print(f"Phone: {customer_phone}")

    db = SessionLocal()
    try:
        orders = get_orders_by_phone(db, phone=customer_phone)

        if not orders:
            return {
                "success": True,
                "message": "No orders found for this phone number",
                "orders": []
            }

        order_list = []
        for order in orders:
            order_summary = get_order_summary(db, order.id)
            order_list.append(order_summary)

        print(f"Found {len(order_list)} orders")

        return {
            "success": True,
            "message": f"Found {len(order_list)} orders",
            "orders": order_list,
        }

    except Exception as exc:
        print(f"Error: {str(exc)}")
        return {"success": False, "error": str(exc)}
    finally:
        db.close()


@function_tool(
    name_override="update_order_status_tool",
    description_override=(
        "Update the status of an existing order. "
        "Status can be: pending, confirmed, shipped, delivered, cancelled. "
        "Use this to confirm orders or update customer about delivery status."
    ),
)
async def update_order_status_tool(order_id: int, status: str) -> dict:
    """
    Update order status
    
    Args:
        order_id: The order ID to update
        status: New status (pending/confirmed/shipped/delivered/cancelled)
    
    Returns:
        Dictionary with success status and updated order details
    """
    
    print("update_order_status_tool called")
    print(f"Order ID: {order_id}")
    print(f"New Status: {status}")

    db = SessionLocal()
    try:
        order = update_order_status(db=db, order_id=order_id, status=status)
        
        if not order:
            return {
                "success": False,
                "error": f"Order with ID {order_id} not found"
            }

        order_summary = get_order_summary(db, order.id)

        print(f"order status updated")

        return {
            "success": True,
            "message": f"Order status updated to {status}",
            "order": order_summary,
        }

    except Exception as exc:
        print(f"Error: {str(exc)}")
        return {"success": False, "error": str(exc)}
    finally:
        db.close()