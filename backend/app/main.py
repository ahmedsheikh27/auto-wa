from fastapi import FastAPI
from app.api.webhook import router as webhook_router
from app.db.base import Base
from app.db.session import Base, engine


app = FastAPI(title="WhatsApp AI Sales Agent MVP")
app.include_router(webhook_router)

@app.get("/")
def home():
    return {"status": "running"}
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)