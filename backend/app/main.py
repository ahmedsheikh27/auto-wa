from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.webhook import router as webhook_router
from app.api.messages import router as message_router
from app.db.session import Base, engine
from app.core.redis import redis_client

app = FastAPI(title="Universal WhatsApp AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router)
app.include_router(message_router)


@app.get("/")
def home():
    return {"status": "running"}


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    redis_client.set("test", "hello")
    print("Redis connected:", redis_client.get("test"))

    print("Server started. Agent schema loaded at import time.")