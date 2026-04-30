from app.models.tables import Order

async def create_order(db, phone, product_name, address):
    order = Order(
        product_name=product_name,
        customer_phone=phone,
        address=address,
        status="confirmed"
    )

    db.add(order)
    await db.commit()
    await db.refresh(order)

    return order