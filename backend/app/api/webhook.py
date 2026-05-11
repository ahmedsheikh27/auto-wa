from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse, Response
from app.agents.main_agent import run_main_agent
from app.services.whatsapp_service import send_whatsapp_message
from app.db.session import SessionLocal
from app.core.config import Settings
from app.services.message_service import save_message
import hmac
import hashlib
from app.services.user_service import get_user, create_user

router = APIRouter()
VERIFY_TOKEN = Settings.ACCESS_TOKEN
APP_SECRET = Settings.APP_SECRET
router = APIRouter(prefix="/webhook", tags=["Webhook"])
db = SessionLocal()


@router.get("/")
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


@router.post("/")
async def whatsapp_webhook(request: Request):
    signature = request.headers.get("X-Hub-Signature-256")
    raw_body = await request.body()

    if not signature:
        raise HTTPException(status_code=403, detail="No signature found")
    signature = signature.replace("sha256=", "")
    expected_sig = hmac.new(APP_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(signature, expected_sig):
        print("Security Alert: Signature mismatch")
        raise HTTPException(status_code=403, detail="Invalid signature")

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
        name = value.get("contacts", [{}])[0].get("profile", {}).get("name")

        if "text" not in message:
            print(f"Non-text message from {phone}")
            return {"status": "non-text ignored"}

        text = message["text"]["body"]
        user = get_user(db, phone)
        if not user:
            print("No user found")
            new_user = create_user(db, user_phone=phone, user_name=name)
            print(
                f"New User created: {new_user.user_name} with phone: {new_user.user_phone}"
            )
            user_id = new_user.id
        else:
            user_id = user.id
        print(f"User ID: {user_id}, Phone: {phone}")

        print(f"\n Incoming from {phone}: {text}")
        save_message(db=db, phone=phone, role="user", content=text, user_id=user_id)
        reply = await run_main_agent(text, customer_phone=phone)
        save_message(db=db, phone=phone, role="bot", content=reply, user_id=user_id)
        print(f"Reply: {reply}\n")

        await send_whatsapp_message(phone, reply)

        return {"status": "ok"}

    except Exception as e:
        print("Error:", e)
        return {"status": "error"}
