from app.core.llm import get_llm

llm = get_llm()


def run_agent(message: str):
    # MVP: simple reasoning first (we will upgrade tools later)
    prompt = f"""
You are a WhatsApp sales assistant.

User message:
{message}
You are an AI assistant for an ecommerce WhatsApp shop.

IMPORTANT RULES:
- If user refers to a product by number (e.g., "no 1", "number 2", "4"), DO NOT classify as FAQ.
- In such cases return intent = ORDER.

Classify the user message into:
- PRODUCT_SEARCH
- ORDER
- FAQ
Reply like a helpful salesman.
"""
    response = llm.invoke(prompt)

    return response
