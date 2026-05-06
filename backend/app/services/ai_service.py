import json
import re
from app.core.llm import get_llm
from app.services.hygraph_service import search_products, search_collections
from app.services.order_service import create_order
from app.models.tables import Message
from app.services.session_service import get_session, update_session, clear_session

llm = get_llm()


async def save_message(db, phone, role, content):
    msg = Message(phone=phone, role=role, content=content)
    db.add(msg)
    db.commit()


def extract_json(text: str):
    try:
        text = re.sub(r"```json|```", "", text).strip()
        return json.loads(text)
    except Exception:
        return None


async def detect_intent(message: str):
    prompt = f"""
You are an AI assistant for an ecommerce jewelry WhatsApp shop.

Classify the user message into ONE of:
- PRODUCT_SEARCH    → user wants to see/buy specific products (e.g. "show me necklaces", "I want earrings")
- COLLECTION_SEARCH → user wants to browse categories/collections (e.g. "what collections do you have", "show me jewelry collections", "bridal collection")
- ORDER             → user is selecting a product by number or saying buy/order
- FAQ               → general questions about delivery, returns, etc.

RULES:
- If user refers to a product/collection by number (e.g. "no 1", "#2"), return ORDER
- "collection", "category", "type", "range", "set" → lean toward COLLECTION_SEARCH
- Specific product types like "necklace", "ring", "earring" → PRODUCT_SEARCH

Message: "{message}"

Respond ONLY in valid JSON:
{{
  "intent": "PRODUCT_SEARCH | COLLECTION_SEARCH | ORDER | FAQ",
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


BASE_PRODUCT_URL = "https://aurora-jewelry-steel.vercel.app/products"
BASE_COLLECTION_URL = "https://aurora-jewelry-steel.vercel.app/collections"


def build_product_url(slug: str):
    return f"{BASE_PRODUCT_URL}/{slug}"


def build_collection_url(slug: str):
    return f"{BASE_COLLECTION_URL}/{slug}"


def extract_index(text: str):
    """Match explicit 'no 5', 'number 3', '#2', or a purely numeric message."""
    match = re.search(r"\b(?:no\.?\s*|number\s*|#)(\d+)\b", text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    stripped = text.strip()
    if re.fullmatch(r"\d+", stripped):
        return int(stripped)
    return None


async def process_message(db, phone: str, message: str):

    session = get_session(phone)
    current_step = session.get("step")

    if current_step == "CONFIRM_SELECTION":
        msg = message.lower().strip()

        if re.search(r"\b(1|order|buy|yes)\b", msg):
            update_session(phone, {"step": "ASK_NAME"})
            return "Great 👍 What's your name?"

        if re.search(r"\b(2|more|see|browse)\b", msg):
            update_session(phone, {"step": "BROWSING"})
            return "Sure 😊 What else would you like to see?"

        return "Reply *1* to order this or *2* to see more products 😊"

    if current_step == "COLLECTION_SELECTED":
        msg = message.lower().strip()

        if re.search(r"\b(1|yes|view|show|see|browse)\b", msg):
            # Show products inside the selected collection
            collection = session.get("selected_collection", {})
            col_products = collection.get("collectionProducts", [])

            if not col_products:
                return "No products found in this collection 😕 Try searching for something else."

            update_session(phone, {"last_products": col_products, "step": None})

            response = f"Here are products from *{collection.get('title')}*:\n\n"
            for i, p in enumerate(col_products, 1):
                url = build_product_url(p["slug"])
                response += f"*{i}.* {p['title']}\n🔗 {url}\n\n"
            response += "Reply with the number to select a product 😊"
            return response

        if re.search(r"\b(2|back|other|different|more collections)\b", msg):
            update_session(phone, {"step": None})
            return "Sure! You can ask me to show all collections or search for something specific 😊"

        return "Reply *1* to view products in this collection or *2* to go back 😊"

    # name asking
    if current_step == "ASK_NAME":
        update_session(phone, {"name": message.strip(), "step": "ASK_ADDRESS"})
        return "📍 What's your delivery address?"

    # address asking
    if current_step == "ASK_ADDRESS":
        update_session(phone, {"address": message.strip(), "step": "CONFIRM"})
        return (
            f"🛒 *Confirm Order:*\n\n"
            f"📦 Product: {session.get('product_name')}\n"
            f"👤 Name: {session.get('name')}\n"
            f"📍 Address: {message.strip()}\n\n"
            f"Reply *YES* to confirm or *NO* to cancel."
        )

    # order confirmation
    if current_step == "CONFIRM":
        msg = message.lower().strip()

        if re.search(r"\b(yes|confirm|ok|sure)\b", msg):
            order = create_order(
                db,
                product_name=session.get("product_name"),
                product_id=session.get("product_id"),
                customer_phone=phone,
                address=session.get("address"),
            )
            clear_session(phone)
            return f"🎉 Order confirmed!\nOrder ID: {order.id}\n\nThank you for shopping with us 💎"

        if re.search(r"\b(no|cancel)\b", msg):
            clear_session(phone)
            return "❌ Order cancelled. Feel free to browse again 😊"

        return "Please reply *YES* to confirm or *NO* to cancel."

    index = extract_index(message)

    if index is not None:
        # collection list
        collections = session.get("last_collections") or []
        if collections:
            if index < 1 or index > len(collections):
                return f"Please choose a number between 1 and {len(collections)} 😊"

            selected_col = collections[index - 1]

            # Fetch collection of products
            from app.services.hygraph_service import get_collection_by_slug

            full_collection = await get_collection_by_slug(selected_col["slug"])

            update_session(
                phone,
                {
                    "step": "COLLECTION_SELECTED",
                    "selected_collection": full_collection,
                    "last_collections": [],  # clear so next index hits products
                },
            )

            col_products = full_collection.get("collectionProducts", [])
            product_count = len(col_products)

            return (
                f"✨ *{full_collection.get('title')}*\n"
                f"{full_collection.get('description', '')}\n\n"
                f"This collection has *{product_count}* product(s).\n\n"
                f"Reply *1* to view products or *2* to go back 😊"
            )

        # product search
        products = session.get("last_products") or []
        if not products:
            return "Please search for a product first 😊"

        if index < 1 or index > len(products):
            return f"Please choose a number between 1 and {len(products)} 😊"

        selected = products[index - 1]
        update_session(
            phone,
            {
                "step": "CONFIRM_SELECTION",
                "product_id": selected["id"],
                "product_name": selected["title"],
                "selected_product": selected,
            },
        )

        url = build_product_url(selected["slug"])
        return (
            f"Nice choice 😍\n\n"
            f"*{selected['title']}*\n"
            f"{selected.get('description', '')}\n"
            f"🔗 {url}\n\n"
            f"Reply *1* to order this or *2* to see more products"
        )

    # intent detection
    intent_data = await detect_intent(message)
    intent = intent_data.get("intent")
    query = intent_data.get("query", message)

    #    collection search
    if intent == "COLLECTION_SEARCH":
        collections = await search_collections(query)

        if not collections:
            return "Sorry, I couldn't find any matching collections 😕 Try searching for products directly!"

        # collectio storage
        update_session(
            phone, {"last_collections": collections, "last_products": [], "step": None}
        )

        response = "✨ Here are our collections:\n\n"
        for i, col in enumerate(collections, 1):
            url = build_collection_url(col["slug"])
            response += f"*{i}.* {col['title']}\n"
            if col.get("description"):
                response += f"    {col['description'][:80]}{'...' if len(col.get('description','')) > 80 else ''}\n"
            response += f"🔗 {url}\n\n"

        response += "Reply with the number to explore a collection 😊"
        return response

    # product search
    if intent == "PRODUCT_SEARCH" or current_step == "BROWSING":
        products = await search_products(query)

        if not products:
            return "Sorry, no products found 😕 Try a different search."

        update_session(
            phone, {"last_products": products, "last_collections": [], "step": None}
        )

        msg = "Here are some options:\n\n"
        for i, p in enumerate(products, 1):
            url = build_product_url(p["slug"])
            msg += f"*{i}.* {p['title']}\n🔗 {url}\n\n"

        msg += "Reply with the number to select a product 😊"
        return msg

    # faq
    return (
        "We offer fast delivery 🚚 and easy returns 🔁\n\n"
        "You can ask me to:\n"
        "• Show *collections* 💎\n"
        "• Search for *products* 🛍️\n"
        "• Place an *order* 📦"
    )
