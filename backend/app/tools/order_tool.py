from agents import function_tool
from app.db.session import SessionLocal
from app.services.order_service import create_order, get_orders_by_phone, update_order_status
from typing import List
from pydantic import BaseModel

class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int = 1

@function_tool(
    name_override="create_order_tool",
    description_override=(
        "Create a new order for a user with multiple products"
    ),
)
async def create_order_tool(
    user_id: int,
    items: List[OrderItemSchema],
    address: str,
    status: str = "pending",
) -> dict:

    print("create order tool called")

    db = SessionLocal()

    try:

        # convert pydantic objects → dict
        formatted_items = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
            }
            for item in items
        ]

        # IMPORTANT:
        # remove await if create_order is normal function
        order = create_order(
            db=db,
            user_id=user_id,
            items=formatted_items,
            status=status,
            address=address,
        )

        return {
            "success": True,
            "message": "Order created successfully",
            "order": {
                "order_id": order.id,
                "user_id": order.user_id,
                "status": order.status,
                "address": order.address,
            },
        }

    except Exception as exc:

        return {
            "success": False,
            "error": str(exc),
        }

    finally:
        db.close()

@function_tool(
    name_override="list_orders_by_phone_tool", description_override="List user orders based on their phone number"
)
async def list_orders_by_phone_tool(customer_phone: str) -> dict:
    """
    List orders filtered by customer phone.
    """
    print("list_orders_by_phone_tool tool called")

    db = SessionLocal()
    try:
        orders = get_orders_by_phone(db, phone=customer_phone)
        return {
            "success": True,
            "orders": [
                {
                    "id": order.id,
                    "product_name": order.product_name,
                    "product_id": order.product_id,
                    "customer_phone": order.customer_phone,
                    "address": order.address,
                    "status": order.status,
                }
                for order in orders
            ],
        }
    except Exception as exc:
        return {"success": False, "error": str(exc)}
    finally:
        db.close()


@function_tool(
    name_override="update_order_status_tool", description_override="Looking to update user's order on the base of their order id"
)
async def update_order_status_tool(order_id: int, status: str) -> dict:
    """
    Update order status (pending/confirmed/cancelled/delivered).
    """
    print(" update_order_status_tool called")
    db = SessionLocal()
    try:
        order = update_order_status(db=db, order_id=order_id, status=status)
        if not order:
            return {"success": False, "error": "Order not found"}
        return {
            "success": True,
            "order_id": order.id,
            "status": order.status,
        }
    except Exception as exc:
        return {"success": False, "error": str(exc)}
    finally:
        db.close()
