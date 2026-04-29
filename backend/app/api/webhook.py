from fastapi import APIRouter, Request
from app.services.ai_service import process_message
from app.services.whatsapp_service import send_whatsapp_message

router = APIRouter()

# Verification (Meta requirement)
@router.get("/webhook")
async def verify(request: Request):
    return "Webhook verified"

# Incoming messages
@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        
        phone = message["from"]
        text = message["text"]["body"]

        # AI processing
        reply = await process_message(text)

        # Send reply back to WhatsApp
        await send_whatsapp_message(phone, reply)

        return {"status": "ok"}

    except Exception as e:
        print("Error:", e)
        return {"status": "error"}