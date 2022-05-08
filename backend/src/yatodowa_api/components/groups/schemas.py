from uuid import UUID

from yatodowa_api.api_validation import StrictBaseModel


class GroupResponse(StrictBaseModel):
    group_id: UUID
    name: str


class GroupsResponse(StrictBaseModel):
    count: int
    groups: list[GroupResponse]
