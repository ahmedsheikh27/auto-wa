from __future__ import annotations

from sqlalchemy.orm import Session

from app.sdk.adapters.postgres import PostgresAdapter
from app.sdk.interfaces import EcommerceAdapter
from app.sdk.schemas import OrderItemInput
from app.sdk.validators import validate_output


class ProductSDK:
    def __init__(self, adapter: EcommerceAdapter):
        self.adapter = adapter

    def list(self) -> list[dict]:
        return [product.to_json_dict() for product in self.adapter.list_products()]

    def search(self, query: str) -> list[dict]:
        return [
            product.to_json_dict()
            for product in self.adapter.search_products(query)
        ]


class CollectionSDK:
    def __init__(self, adapter: EcommerceAdapter):
        self.adapter = adapter

    def list(self) -> list[dict]:
        return [
            collection.to_json_dict()
            for collection in self.adapter.list_collections()
        ]

    def search(self, query: str) -> list[dict]:
        return [
            collection.to_json_dict()
            for collection in self.adapter.search_collections(query)
        ]

    def get_products(self, slug: str) -> dict | None:
        collection = self.adapter.get_collection_products(slug)
        return collection.to_json_dict() if collection else None


class UserSDK:
    def __init__(self, adapter: EcommerceAdapter):
        self.adapter = adapter

    def get_by_phone(self, phone: str) -> dict | None:
        user = self.adapter.get_user_by_phone(phone)
        return user.to_json_dict() if user else None

    def create(self, user_name: str | None, user_phone: str) -> dict:
        return self.adapter.create_user(user_name, user_phone).to_json_dict()

    def get_or_create(self, user_name: str | None, user_phone: str) -> dict:
        user = self.get_by_phone(user_phone)
        if user:
            return user
        return self.create(user_name=user_name, user_phone=user_phone)


class MessageSDK:
    def __init__(self, adapter: EcommerceAdapter):
        self.adapter = adapter

    def save(self, phone: str, role: str, content: str, user_id: int) -> dict:
        return self.adapter.save_message(
            phone=phone,
            role=role,
            content=content,
            user_id=user_id,
        ).to_json_dict()


class OrderSDK:
    def __init__(self, adapter: EcommerceAdapter):
        self.adapter = adapter

    def create(
        self,
        user_id: int,
        items: list[dict],
        address: str,
        status: str = "pending",
    ) -> dict:
        parsed_items = [validate_output(OrderItemInput, item) for item in items]
        order = self.adapter.create_order(
            user_id=user_id,
            items=parsed_items,
            address=address,
            status=status,
        )
        return order.to_json_dict()

    def list_by_phone(self, phone: str) -> list[dict]:
        return [
            order.to_json_dict()
            for order in self.adapter.list_orders_by_phone(phone)
        ]

    def update_status(self, order_id: int, status: str) -> dict | None:
        order = self.adapter.update_order_status(order_id, status)
        return order.to_json_dict() if order else None


class EcommerceSDK:
    def __init__(self, adapter: EcommerceAdapter):
        self.adapter = adapter
        self.adapter.verify_schema()
        self.products = ProductSDK(adapter)
        self.collections = CollectionSDK(adapter)
        self.users = UserSDK(adapter)
        self.messages = MessageSDK(adapter)
        self.orders = OrderSDK(adapter)


def create_sdk(db: Session) -> EcommerceSDK:
    return EcommerceSDK(PostgresAdapter(db))
