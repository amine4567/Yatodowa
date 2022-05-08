from enum import Enum

from pydantic import BaseModel, Extra


class StrictBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid


class ErrorType(str, Enum):
    GENERIC = "generic_error"
    VALIDATION = "validation_error"


class APICallError(StrictBaseModel):
    type: ErrorType
    subtype: str | None
    message: str
