from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.sdk.exceptions import SchemaValidationError

ModelT = TypeVar("ModelT", bound=BaseModel)


def validate_output(model: type[ModelT], data: object) -> ModelT:
    try:
        if hasattr(model, "model_validate"):
            return model.model_validate(data)
        return model.parse_obj(data)
    except ValidationError as exc:
        raise SchemaValidationError(
            f"Database output does not match {model.__name__}: {exc}"
        ) from exc


def validate_list(model: type[ModelT], rows: list[object]) -> list[ModelT]:
    return [validate_output(model, row) for row in rows]
