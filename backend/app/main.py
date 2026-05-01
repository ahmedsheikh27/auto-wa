from fastapi import FastAPI
from app.api.webhook import router as webhook_router
from app.api.agent import router as agent_router
from app.api.products import router as products_router
from app.api.orders import router as orders_router
from app.api.messages import router as messages_router
from app.db.session import Base, engine


app = FastAPI(title="WhatsApp AI Sales Agent MVP")
app.include_router(webhook_router)
app.include_router(agent_router)
app.include_router(products_router)
app.include_router(orders_router)
app.include_router(messages_router)
@app.get("/")
def home():
    return {"status": "running"}
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)