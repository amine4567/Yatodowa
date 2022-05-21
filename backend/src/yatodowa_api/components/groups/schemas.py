from uuid import UUID

from yatodowa_api.validation import StrictBaseModel, validators


class GroupResponseModel(StrictBaseModel):
    group_id: UUID
    name: str


class MultiGroupsResponseModel(StrictBaseModel):
    groups: list[GroupResponseModel]
    count: int | None

    _count_validator: classmethod = validators.count_validator("groups", "count")
