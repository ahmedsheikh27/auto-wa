from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.webhook import router as webhook_router
from app.api.products import router as products_router
from app.api.messages import router as message_router
from app.api.collection import router as collection_router
from app.db.session import Base, engine



app = FastAPI(title="WhatsApp AI Sales Agent MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router)
app.include_router(products_router)
app.include_router(message_router)
app.include_router(collection_router)
@app.get("/")
def home():
    return {"status": "running"}
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
