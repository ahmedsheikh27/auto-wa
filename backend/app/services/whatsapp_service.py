import httpx
from app.core.config import Settings

ACCESS_TOKEN = Settings.ACCESS_TOKEN
PHONE_NUMBER_ID = Settings.PHONE_NUMBER_ID

async def send_whatsapp_message(to: str, message: str):
    url = f'https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages'
    

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(url, headers=headers, json=payload)

        print("📤 WhatsApp API Response:", res.status_code, res.text)