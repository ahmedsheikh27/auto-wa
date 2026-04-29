import httpx
from app.core.config import settings

ACCESS_TOKEN = settings.ACCESS_TOKEN
PHONE_NUMBER_ID = settings.PHONE_NUMBER_ID

async def send_whatsapp_message(to: str, message: str):
    url = settings.WHATSAP_BASE_URL

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload, headers=headers)