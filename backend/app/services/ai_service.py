from app.agents.agent import run_agent

async def process_message(message: str):
    response = run_agent(message)
    return response