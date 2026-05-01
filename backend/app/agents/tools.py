from app.services.product_service import search_products
from app.services.order_service import create_order

async def product_search_tool(db, query):
    products = await search_products(db, query)

    if not products:
        return "No products found. Try another keyword."

    response = "🔥 Available Products:\n\n"
    for p in products[:5]:
        response += f"{p.name}\n💰 Rs {p.price}\n\n"

    return response

async def order_tool(db, phone, product):
    await create_order(db, phone, product, "Pending Address")

    return f"""
✅ Order placed for {product}

Please reply with your address 📍
"""