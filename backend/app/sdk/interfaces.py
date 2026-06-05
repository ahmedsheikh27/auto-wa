from abc import ABC, abstractmethod

from app.sdk.schemas import (
    CollectionOut,
    MessageOut,
    OrderItemInput,
    OrderOut,
    ProductOut,
    UserOut,
)


class EcommerceAdapter(ABC):
    @abstractmethod
    def verify_schema(self) -> None:
        """Validate that the connected database has the required Mode 1 schema."""

    @abstractmethod
    def list_products(self) -> list[ProductOut]:
        """Return all products using the SDK product output schema."""

    @abstractmethod
    def search_products(self, query: str) -> list[ProductOut]:
        """Search products using the SDK product output schema."""

    @abstractmethod
    def list_collections(self) -> list[CollectionOut]:
        """Return all collections using the SDK collection output schema."""

    @abstractmethod
    def search_collections(self, query: str) -> list[CollectionOut]:
        """Search collections using the SDK collection output schema."""

    @abstractmethod
    def get_collection_products(self, slug: str) -> CollectionOut | None:
        """Return one collection with its products."""

    @abstractmethod
    def get_user_by_phone(self, phone: str) -> UserOut | None:
        """Return one user by phone number."""

    @abstractmethod
    def create_user(self, user_name: str | None, user_phone: str) -> UserOut:
        """Create a user and return the SDK user output schema."""

    @abstractmethod
    def save_message(
        self,
        phone: str,
        role: str,
        content: str,
        user_id: int,
    ) -> MessageOut:
        """Persist a chat message and return the SDK message output schema."""

    @abstractmethod
    def create_order(
        self,
        user_id: int,
        items: list[OrderItemInput],
        address: str,
        status: str = "pending",
    ) -> OrderOut:
        """Create an order with items and return the SDK order output schema."""

    @abstractmethod
    def list_orders_by_phone(self, phone: str) -> list[OrderOut]:
        """Return all orders for a phone number."""

    @abstractmethod
    def update_order_status(self, order_id: int, status: str) -> OrderOut | None:
        """Update order status and return the SDK order output schema."""
