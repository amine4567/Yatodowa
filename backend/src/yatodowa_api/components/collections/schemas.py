from uuid import UUID

from yatodowa_api.common.schemas import StrictBaseModel


class CollectionQueryBody(StrictBaseModel):
    name: str
    group_id: UUID | None


class CollectionResponse(StrictBaseModel):
    collection_id: UUID
    name: str
    group_id: UUID | None
