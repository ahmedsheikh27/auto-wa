from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, Response
from app.services.ai_service import process_message
from app.services.whatsapp_service import send_whatsapp_message
from app.db.session import SessionLocal
from app.core.config import Settings
from app.models.tables import Message
from app.services.message_service import save_message
router = APIRouter()
VERIFY_TOKEN = Settings.ACCESS_TOKEN


@router.get("/webhook")
async def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    print(f"Got: mode={mode} token={token}")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("SUCCESS: Returning challenge")
        return PlainTextResponse(content=challenge, status_code=200)
    
    print("FAIL: Token mismatch or wrong mode")
    return Response(status_code=403)


async def save_message(db, phone, role, content):
    msg = Message(
        phone=phone,
        role=role,
        content=content
    )
    db.add(msg)
    db.commit()


@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()

    print("RAW WEBHOOK DATA:")
    print(data)

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            print("No message found in payload")
            return {"status": "no message"}

        message = value["messages"][0]

        phone = message.get("from")

        if "text" not in message:
            print(f"Non-text message from {phone}")
            return {"status": "non-text ignored"}

        text = message["text"]["body"]

        print(f"\n Incoming from {phone}: {text}")

        with SessionLocal() as db:
            await save_message(db, phone, text, "user")
            reply = await process_message(db, phone, text)
            await save_message(db, phone, reply, "bot")

        print(f"Reply: {reply}\n")

        await send_whatsapp_message(phone, reply)

        return {"status": "ok"}

    except Exception as e:
        print("Error:", e)
        return {"status": "error"}