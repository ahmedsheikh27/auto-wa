from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.message_service import get_messages

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.get("/")
def list_messages(db: Session = Depends(get_db)):
    return get_messages(db)