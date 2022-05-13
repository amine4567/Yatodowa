from enum import Enum

from pydantic import BaseModel, Extra, validator


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


class APICallErrors(StrictBaseModel):
    errors: list[APICallError]
    errors_count: int | None

    @validator("errors_count", always=True)
    def compute_count(cls, _, values: dict) -> int:
        return len(values["errors"])
