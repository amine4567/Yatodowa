from uuid import UUID

from yatodowa_api.validation import StrictBaseModel, validators


class GroupResponse(StrictBaseModel):
    group_id: UUID
    name: str


class GroupsResponse(StrictBaseModel):
    groups: list[GroupResponse]
    count: int | None

    _count_validator: classmethod = validators.count_validator("groups", "count")
