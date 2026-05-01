import json
import re
from app.core.llm import get_llm
from app.services.hygraph_service import search_products
from app.services.order_service import create_order
from app.models.tables import Message
import re
from app.services.session_service import get_session, update_session, clear_session

llm = get_llm()


async def save_message(db, phone, role, content):
    msg = Message(phone=phone, role=role, content=content)
    db.add(msg)
    db.commit()


def extract_json(text: str):
    try:
        # remove ```json blocks if present
        text = re.sub(r"```json|```", "", text).strip()
        return json.loads(text)
    except Exception:
        return None


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
    content = (
        response
        if isinstance(response, str)
        else getattr(response, "content", str(response))
    )
    parsed = extract_json(content)

    if not parsed:
        return {"intent": "FAQ", "query": message}

    return parsed


def extract_product_id(text: str):
    match = re.search(r"\(ID:\s*(.*?)\)", text)
    return match.group(1) if match else None



async def process_message(db, phone: str, message: str):

    intent_data = await detect_intent(message)
    intent = intent_data.get("intent")
    query = intent_data.get("query", message)

    session = get_session(phone)

    # =========================
    # STEP 1: PRODUCT SELECTED
    # =========================
    product_id = extract_product_id(message)

    if product_id:
        products = session.get("last_products", [])

        product_name = None
        for p in products:
            if p["id"] == product_id:
                product_name = p["title"]
                break

        update_session(phone, {
            "step": "ASK_NAME",
            "product_id": product_id,
            "product_name": product_name or "Unknown"
        })

        return "Great 👍 What's your name?"

    # =========================
    # STEP 2: ASK NAME
    # =========================
    if session.get("step") == "ASK_NAME":
        update_session(phone, {"name": message, "step": "ASK_ADDRESS"})
        return "Perfect 👍 Now send your delivery address."

    # =========================
    # STEP 3: ASK ADDRESS
    # =========================
    if session.get("step") == "ASK_ADDRESS":
        update_session(phone, {"address": message, "step": "CONFIRM"})

        return f"""
🛒 Confirm Order:

📦 Product ID: {session.get('product_id')}
👤 Name: {session.get('name')}
📍 Address: {message}

Reply YES to confirm or NO to cancel.
"""

    # =========================
    # STEP 4: CONFIRM ORDER
    # =========================
    if message.lower() == "yes" and session.get("step") == "CONFIRM":

        order = create_order(
            db,
            product_name=session.get("product_name", "Unknown"),
            product_id=session["product_id"],
            customer_phone=phone,
            address=session["address"],
        )

        clear_session(phone)
        return f"🎉 Order confirmed! We will contact you soon.\nOrder ID: {order.id}"

    if message.lower() == "no":
        clear_session(phone)
        return "❌ Order cancelled."

    # =========================
    # STEP 5: PRODUCT SEARCH FLOW
    # =========================
    if intent == "PRODUCT_SEARCH":
        products = await search_products(query)

        if not products:
            return "Sorry, no products found 😕"

        response = "Here are some options:\n\n"

        for p in products[:3]:
            response += f"{p['title']} (ID: {p['id']})\n"

        response += "\nReply with product ID to continue order 👍"

        return response

    # =========================
    # DEFAULT (FAQ)
    # =========================
    return "We offer fast delivery 🚚 and easy returns 🔁. What would you like to buy?"
