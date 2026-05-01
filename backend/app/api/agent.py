from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.ai_service import process_message

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/chat")
async def chat(data: dict, db: Session = Depends(get_db)):
    phone = data.get("phone", "web-user")
    message = data.get("message")

    reply = await process_message(db, phone, message)

    return {"reply": reply}