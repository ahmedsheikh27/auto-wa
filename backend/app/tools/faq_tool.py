from agents import function_tool
@function_tool(
    name_override="faq_lookup_tool", description_override="Lookup frequently asked messages."
)
async def faq_lookup_tool(message: str) -> str:
    message = message.lower()

    if "delivery" in message or "shipping" in message or "arrive" in message:
        return (
            "🚚 Delivery usually takes 2–5 business days depending on your location. "
            "You will receive a tracking update once your order is shipped."
        )

    elif "payment" in message or "pay" in message or "cod" in message:
        return (
            "💳 We support Cash on Delivery (COD) and online payment methods depending on your region. "
            "You can choose your preferred option at checkout."
        )

    elif "return" in message or "refund" in message or "exchange" in message:
        return (
            "🔁 You can request a return or exchange within 7 days of delivery. "
            "The product must be unused and in original packaging."
        )

    elif "order" in message or "track" in message or "status" in message:
        return (
            "📦 You can track your order once it is shipped. "
            "Our team will also send you updates via WhatsApp."
        )

    elif "available" in message or "stock" in message or "product" in message:
        return (
            "🛍️ You can browse all available products in the catalog. "
            "Just tell me what you're looking for and I’ll help you find it."
        )

    elif "location" in message or "address" in message or "store" in message:
        return (
            "📍 We operate online only, but our warehouse ships nationwide across Pakistan."
        )

    elif "how long" in message or "time" in message:
        return (
            "⏱️ Delivery usually takes 2–5 business days depending on your city."
        )

    return (
        "🤖 I’m sorry, I don’t have that information right now. "
        "Please ask about orders, delivery, payments, or returns."
    )