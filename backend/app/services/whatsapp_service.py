import httpx
from app.core.config import Settings

ACCESS_TOKEN = "EAAShzC0QhQgBRaHjdUrAuG8fiUSZBj1GWaaZBljccKxZCXgD9FPB6cU54KVT1ZCGVyj6cmJQDSFZA4N5ZBpGGnEQ4nnTc4xMiiqr5jHfabqPbPVVSX714bL7Jc1sQGulxHZCQ2686hHwsZBVIoQ8qSdkZC9ZCZB8y5m9x8yZAFduhB4w3QwLf4moYKYbrO2AxcIphgVLBFK8mH5sMxalpVMHw07iy99RtEiZB0UZAwxDQAMwoP"
PHONE_NUMBER_ID = Settings.PHONE_NUMBER_ID

async def send_whatsapp_message(to: str, message: str):
    url = f'https://graph.facebook.com/v25.0/{183261234863210}/messages'

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