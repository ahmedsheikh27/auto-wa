class SDKError(Exception):
    """Base exception for SDK failures."""


class DatabaseSchemaError(SDKError):
    """Raised when the connected database does not match the required schema."""


class SchemaValidationError(SDKError):
    """Raised when database output cannot be converted to the SDK output schema."""
