from datetime import datetime

from sqlalchemy import inspect, select
from sqlalchemy.orm import Session

from app.models.tables import Collection, Message, Order, OrderItem, Product, User
from app.sdk.exceptions import DatabaseSchemaError
from app.sdk.interfaces import EcommerceAdapter
from app.sdk.schemas import (
    CollectionOut,
    MessageOut,
    OrderItemInput,
    OrderOut,
    ProductOut,
    UserOut,
)
from app.sdk.validators import validate_list, validate_output


REQUIRED_SCHEMA = {
    "users": {"id", "user_name", "user_phone"},
    "products": {"id", "title", "description", "collection_id"},
    "collections": {"id", "title", "description", "slug"},
    "orders": {"id", "user_id", "address", "status", "created_at"},
    "order_items": {"id", "order_id", "product_id", "quantity"},
    "messages": {"id", "user_id", "phone", "role", "content", "created_at"},
}


class PostgresAdapter(EcommerceAdapter):
    def __init__(self, db: Session):
        self.db = db

    def verify_schema(self) -> None:
        inspector = inspect(self.db.bind)
        existing_tables = set(inspector.get_table_names())
        missing_tables = set(REQUIRED_SCHEMA) - existing_tables

        if missing_tables:
            raise DatabaseSchemaError(
                f"Missing required tables: {sorted(missing_tables)}"
            )

        for table_name, required_columns in REQUIRED_SCHEMA.items():
            existing_columns = {
                column["name"] for column in inspector.get_columns(table_name)
            }
            missing_columns = required_columns - existing_columns

            if missing_columns:
                raise DatabaseSchemaError(
                    f"Table '{table_name}' is missing columns: {sorted(missing_columns)}"
                )

    def list_products(self) -> list[ProductOut]:
        products = self.db.query(Product).all()
        return validate_list(ProductOut, [self._product_data(product) for product in products])

    def search_products(self, query: str) -> list[ProductOut]:
        stmt = select(Product).where(Product.title.ilike(f"%{query}%"))
        products = self.db.execute(stmt).scalars().all()
        return validate_list(ProductOut, [self._product_data(product) for product in products])

    def list_collections(self) -> list[CollectionOut]:
        collections = self.db.query(Collection).all()
        return validate_list(
            CollectionOut,
            [self._collection_data(collection, include_products=False) for collection in collections],
        )

    def search_collections(self, query: str) -> list[CollectionOut]:
        stmt = select(Collection).where(Collection.title.ilike(f"%{query}%"))
        collections = self.db.execute(stmt).scalars().all()
        return validate_list(
            CollectionOut,
            [self._collection_data(collection, include_products=True) for collection in collections],
        )

    def get_collection_products(self, slug: str) -> CollectionOut | None:
        collection = self.db.query(Collection).filter(Collection.slug == slug).first()

        if not collection:
            return None

        return validate_output(
            CollectionOut,
            self._collection_data(collection, include_products=True),
        )

    def get_user_by_phone(self, phone: str) -> UserOut | None:
        stmt = select(User).where(User.user_phone == phone)
        user = self.db.execute(stmt).scalar_one_or_none()

        if not user:
            return None

        return validate_output(UserOut, self._user_data(user))

    def create_user(self, user_name: str | None, user_phone: str) -> UserOut:
        user = User(user_name=user_name, user_phone=user_phone)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return validate_output(UserOut, self._user_data(user))

    def save_message(
        self,
        phone: str,
        role: str,
        content: str,
        user_id: int,
    ) -> MessageOut:
        message = Message(
            phone=phone,
            role=role,
            content=content,
            user_id=user_id,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return validate_output(MessageOut, self._message_data(message))

    def create_order(
        self,
        user_id: int,
        items: list[OrderItemInput],
        address: str,
        status: str = "pending",
    ) -> OrderOut:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise DatabaseSchemaError(f"User with id {user_id} was not found.")

        for item in items:
            product = self.db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise DatabaseSchemaError(
                    f"Product with id {item.product_id} was not found."
                )

        order = Order(
            user_id=user_id,
            status=status,
            address=address,
            created_at=datetime.utcnow(),
        )
        self.db.add(order)
        self.db.flush()

        for item in items:
            self.db.add(
                OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                )
            )

        self.db.commit()
        self.db.refresh(order)
        return validate_output(OrderOut, self._order_data(order))

    def list_orders_by_phone(self, phone: str) -> list[OrderOut]:
        user = self.db.execute(
            select(User).where(User.user_phone == phone)
        ).scalar_one_or_none()

        if not user:
            return []

        orders = self.db.execute(
            select(Order).where(Order.user_id == user.id)
        ).scalars().all()

        return validate_list(OrderOut, [self._order_data(order) for order in orders])

    def update_order_status(self, order_id: int, status: str) -> OrderOut | None:
        order = self.db.execute(
            select(Order).where(Order.id == order_id)
        ).scalar_one_or_none()

        if not order:
            return None

        order.status = status
        self.db.commit()
        self.db.refresh(order)
        return validate_output(OrderOut, self._order_data(order))

    def _user_data(self, user: User) -> dict:
        return {
            "id": user.id,
            "user_name": user.user_name,
            "user_phone": user.user_phone,
        }

    def _product_data(self, product: Product) -> dict:
        return {
            "id": product.id,
            "title": product.title,
            "description": product.description,
            "collection_id": product.collection_id,
        }

    def _collection_data(
        self,
        collection: Collection,
        include_products: bool,
    ) -> dict:
        return {
            "id": collection.id,
            "title": collection.title,
            "description": collection.description,
            "slug": collection.slug,
            "products": [
                self._product_data(product) for product in collection.products
            ] if include_products else [],
        }

    def _message_data(self, message: Message) -> dict:
        return {
            "id": message.id,
            "user_id": message.user_id,
            "phone": message.phone,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at,
        }

    def _order_data(self, order: Order) -> dict:
        return {
            "id": order.id,
            "user_id": order.user_id,
            "address": order.address,
            "status": order.status,
            "created_at": order.created_at,
            "items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "product_name": item.product.title if item.product else None,
                    "description": item.product.description if item.product else None,
                }
                for item in order.items
            ],
        }
