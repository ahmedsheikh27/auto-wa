from app.core.llm import get_llm

llm = get_llm()


def run_agent(message: str):
    # MVP: simple reasoning first (we will upgrade tools later)
    prompt = f"""
You are a WhatsApp sales assistant.

User message:
{message}

Decide:
1. Is it product request?
2. Is it order request?
3. Or FAQ?

Reply like a helpful salesman.
"""
    response = llm.invoke(prompt)

    return response
