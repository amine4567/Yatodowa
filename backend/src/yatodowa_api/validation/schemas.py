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


class APICallError(StrictBaseModel):
    type: ErrorType
    subtype: str | None
    message: str


class APICallErrors(StrictBaseModel):
    errors: list[APICallError]
    errors_count: int | None

    _count_validator: classmethod = validators.count_validator("errors", "errors_count")
