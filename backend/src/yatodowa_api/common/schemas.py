from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra


class CustomBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid


class ErrorType(str, Enum):
    GENERIC = "generic_error"
    VALIDATION = "validation_error"


class APICallError(CustomBaseModel):
    type: ErrorType
    subtype: Optional[str]
    message: str
