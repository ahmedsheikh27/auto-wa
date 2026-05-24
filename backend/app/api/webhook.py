from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse, Response
from app.agents.main_agent import run_agent
from app.services.whatsapp_service import send_whatsapp_message
from app.db.session import SessionLocal
from app.core.config import Settings
from app.services.message_service import save_message
import hmac
import hashlib
from app.services.user_service import get_user, create_user

router = APIRouter(prefix="/webhook", tags=["Webhook"])

VERIFY_TOKEN = Settings.ACCESS_TOKEN
APP_SECRET = Settings.APP_SECRET
db = SessionLocal()


@router.get("/")
async def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    print(f"Verify: mode={mode} token={token}")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge, status_code=200)

    return Response(status_code=403)


@router.post("/")
async def whatsapp_webhook(request: Request):
    signature = request.headers.get("X-Hub-Signature-256")
    raw_body = await request.body()

    if not signature:
        raise HTTPException(status_code=403, detail="No signature found")

    signature = signature.replace("sha256=", "")
    expected_sig = hmac.new(APP_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(signature, expected_sig):
        raise HTTPException(status_code=403, detail="Invalid signature")

    data = await request.json()
    print("Webhook received:", data)

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            return {"status": "no message"}

        message = value["messages"][0]
        phone = message.get("from")
        name = value.get("contacts", [{}])[0].get("profile", {}).get("name")

        if "text" not in message:
            return {"status": "non-text ignored"}

        text = message["text"]["body"]

        # Get or create user
        user = get_user(db, phone)
        if not user:
            user = create_user(db, user_phone=phone, user_name=name)
            print(f"New user: {user.user_name} ({user.user_phone})")

        print(f"Incoming [{phone}]: {text}")

        save_message(db=db, phone=phone, role="user", content=text, user_id=user.id)

        reply = await run_agent(text, customer_phone=phone)

        save_message(db=db, phone=phone, role="bot", content=reply, user_id=user.id)

        print(f"Reply: {reply}")

        await send_whatsapp_message(phone, reply)

        return {"status": "ok"}

    except Exception as e:
        print("Webhook error:", e)
        return {"status": "error"}