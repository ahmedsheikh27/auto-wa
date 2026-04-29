from fastapi import FastAPI
from app.api.webhook import router as webhook_router

app = FastAPI(title="WhatsApp AI Sales Agent MVP")

app.include_router(webhook_router)

@app.get("/")
def home():
    return {"status": "running"}