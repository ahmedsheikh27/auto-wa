from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.main_agent import run_agent

router = APIRouter(prefix="/messages", tags=["Messages"])


class MessageRequest(BaseModel):
    message: str
    phone: str | None = "test_user"


@router.post("/")
async def send_messages(body: MessageRequest):
    result = await run_agent(message=body.message, customer_phone=body.phone)
    return {"response": result}