import json
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class SDKModel(BaseModel):
    def to_json_dict(self) -> dict[str, Any]:
        if hasattr(self, "model_dump"):
            return self.model_dump(mode="json")
        return json.loads(self.json())


class UserOut(SDKModel):
    id: int
    user_name: str | None = None
    user_phone: str


class ProductOut(SDKModel):
    id: int
    title: str
    description: str | None = None
    collection_id: int | None = None


class CollectionOut(SDKModel):
    id: int
    title: str
    description: str | None = None
    slug: str | None = None
    products: list[ProductOut] = Field(default_factory=list)


class OrderItemInput(SDKModel):
    product_id: int
    quantity: int = 1


class OrderItemOut(SDKModel):
    id: int | None = None
    product_id: int
    quantity: int
    product_name: str | None = None
    description: str | None = None


class OrderOut(SDKModel):
    id: int
    user_id: int
    address: str | None = None
    status: str
    created_at: datetime | None = None
    items: list[OrderItemOut] = Field(default_factory=list)


class MessageOut(SDKModel):
    id: int
    user_id: int
    phone: str
    role: str
    content: str
    created_at: datetime | None = None
