from uuid import UUID

from yatodowa_api.common.schemas import StrictBaseModel


class GroupResponse(StrictBaseModel):
    group_id: UUID
    name: str
