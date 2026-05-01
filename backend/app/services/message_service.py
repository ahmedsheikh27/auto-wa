from app.models.tables import Message
from sqlalchemy import select

async def save_message(db, phone, content, sender):
    msg = Message(
        phone=phone,
        content=content,
        sender=sender
    )

    db.add(msg)
    db.commit()
    db.refresh(msg)

    return msg


def get_messages(db):
    return db.query(Message).all()