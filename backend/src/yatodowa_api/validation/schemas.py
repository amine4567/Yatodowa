from enum import Enum

from pydantic import BaseModel, Extra
from yatodowa_api.validation import validators


class StrictBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True


class ErrorType(str, Enum):
    GENERIC = "generic_error"
    VALIDATION = "validation_error"
    MISSING_RESOURCE = "missing_resource_error"


class APICallError(StrictBaseModel):
    type: ErrorType
    subtype: str | None
    message: str


class APICallErrors(StrictBaseModel):
    errors: list[APICallError]
    errors_count: int | None

    _validate_count: classmethod = validators.validate_count("errors", "errors_count")
