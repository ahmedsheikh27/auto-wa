from fastapi import APIRouter
from pydantic import BaseModel
from app.core.config import Settings

PHONE_NUMBER = Settings.PHONE_NUMBER

from agents import Runner
from app.agents.main_agent import run_main_agent

router = APIRouter(prefix="/messages", tags=["Messages"])


class MessageRequest(BaseModel):
    message: str
    phone: str = PHONE_NUMBER


@router.post("/")
async def send_messages(body: MessageRequest):
    result = await run_main_agent(message=body.message, customer_phone=body.phone)
    return {'response': result}
