from uuid import UUID

from pydantic import validator
from yatodowa_api.api_validation import StrictBaseModel


class GroupResponse(StrictBaseModel):
    group_id: UUID
    name: str


class GroupsResponse(StrictBaseModel):
    groups: list[GroupResponse]
    count: int | None

    @validator("count", always=True)
    def compute_count(cls, _, values: dict) -> int:
        return len(values["groups"])
