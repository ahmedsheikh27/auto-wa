from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from app.db.session import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    customer_phone = Column(String)
    address = Column(String)
    status = Column(String, default="pending")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    category = Column(String)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    phone = Column(String, index=True)

    role = Column(String)  
    # "user" or "agent"

    content = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)