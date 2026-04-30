import json
import re
from app.core.llm import get_llm
from app.services.product_service import search_products
from app.services.order_service import create_order
from app.models.tables import Message
llm = get_llm()

async def save_message(db, phone, role, content):
    msg = Message(
        phone=phone,
        role=role,
        content=content
    )
    db.add(msg)
    db.commit()

def extract_json(text: str):
    try:
        # remove ```json blocks if present
        text = re.sub(r"```json|```", "", text).strip()
        return json.loads(text)
    except Exception:
        return None


# 🤖 INTENT DETECTION (IMPROVED)
async def detect_intent(message: str):
    prompt = f"""
You are an AI assistant for an ecommerce WhatsApp shop.

Classify the user message into ONE of these intents:
- PRODUCT_SEARCH
- ORDER
- FAQ

Also extract the main query.

Message: "{message}"

Respond ONLY in valid JSON:
{{
  "intent": "PRODUCT_SEARCH | ORDER | FAQ",
  "query": "cleaned user intent"
}}
"""

    response = llm.invoke(prompt)
    content = response if isinstance(response, str) else getattr(response, "content", str(response))
    parsed = extract_json(content)

    if not parsed:
        return {"intent": "FAQ", "query": message}

    return parsed


# 🚀 MAIN PROCESS FUNCTION
async def process_message(db, phone: str, message: str):
    intent_data = await detect_intent(message)

    intent = intent_data.get("intent")
    query = intent_data.get("query", message)

    # 🛒 PRODUCT SEARCH
    if intent == "PRODUCT_SEARCH":
        products = search_products(db, query)

        if not products:
            return "Sorry, I couldn't find that product. Want me to suggest something similar? 👍"

        response = "Here are some options:\n\n"

        for p in products[:3]:
            response += f"• {p.name} - Rs {p.price}\n"

        response += "\nReply with the product name to order 👍"

        return response

    # 📦 ORDER
    elif intent == "ORDER":
        if not query:
            return "Which product would you like to order? 😊"

        # ⚠️ TEMP HARDCODE (we fix in Step 8)
        address = "Not Provided"

        order = create_order(db, phone, query, address)

        return f"Your order for '{query}' has been placed 🎉\nWe will contact you shortly."

    # ❓ FAQ
    else:
        return "We offer fast delivery 🚚 and easy returns 🔁. What product are you looking for?"