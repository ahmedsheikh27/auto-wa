from app.models.tables import Message
from sqlalchemy import select

from app.models.tables import Message

def save_message(db, phone, role, content, user_id: int):
    msg = Message(
        phone=phone,
        role=role,
        content=content,
        user_id=user_id
    )

    db.add(msg)

    db.commit()
    db.refresh(msg)

    return msg


def get_messages(db):
    return db.query(Message).all()