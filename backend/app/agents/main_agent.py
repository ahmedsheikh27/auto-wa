from agents import Agent, OpenAIChatCompletionsModel, Runner, handoff, RunContextWrapper
from app.agents.faq_agent import faq_agent
from app.agents.order_agent import order_agent
from app.agents.product_agent import products_agent
from app.core.config import Settings
from app.services.session_service import get_session, save_session

client = Settings.CLIENT


def on_product_handoff(ctx: RunContextWrapper[None]):
    print("product agent active")


def on_order_handoff(ctx: RunContextWrapper[None]):
    print("order agent active")


def on_faq_handoff(ctx: RunContextWrapper[None]):
    print("faq agent active")


main_agent = Agent(
    name="Main_WhatsApp_Triage_Agent",
    handoff_description="You are the main agent responsible for triaging user requests and routing to the correct specialist agents.",
    instructions="""
You are the main WhatsApp ecommerce assistant.

Your job is to understand each user message and route to the correct specialist:
- products_agent: product browsing, searching, recommendations, collections
- order_agent: order placement, checkout, order updates/cancellation
- faq_agent: shipping, returns, payment methods, policies

Rules:
- Keep replies short, human, and WhatsApp-friendly.
- If the user intent is unclear, ask one short clarifying question.
- Always handoff to a specialist when the request belongs to it.
- Do not invent product, order, or policy data.
""",
    model=OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client),
    handoffs=[
        handoff(products_agent, on_handoff=on_product_handoff),
        handoff(order_agent, on_handoff=on_order_handoff),
        handoff(faq_agent, on_handoff=on_faq_handoff),
    ],
)
print("main agent called")


async def run_main_agent(
    message: str,
    customer_phone: str | None = None
) -> str:

    session = get_session(customer_phone)

    print(f"Session for {customer_phone}: {session}")

    if not session:

        session = {
            "messages": [],
            "cart": [],
            "current_step": None,
            "customer_phone": customer_phone
        }

    messages = session["messages"]

    messages.append({
        "role": "user",
        "content": message
    })

    messages = messages[-20:]

    session["messages"] = messages

    result = await Runner.run(
        main_agent,
        input=messages
    )

    final_output = str(result.final_output)

    # Add assistant response
    messages.append({
        "role": "assistant",
        "content": final_output
    })

    session["messages"] = messages[-20:]

    save_session(customer_phone, session)

    return final_output