from app.models.tables import  User
from sqlalchemy import select
def get_user(db, phone: str):
    """Get existing user by phone or create new one"""
    stmt = select(User).where(User.user_phone == phone)
    result = db.execute(stmt)
    user = result.scalar_one_or_none()
    return user
def create_user(db, user_name: str, user_phone: str):
    """Create new user"""
    user = User(
        user_name=user_name,
        user_phone=user_phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user