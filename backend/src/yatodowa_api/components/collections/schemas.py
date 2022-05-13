from uuid import UUID

from yatodowa_api.api_validation import StrictBaseModel, validators


class CollectionQueryBody(StrictBaseModel):
    name: str
    group_id: UUID | None


class CollectionResponse(StrictBaseModel):
    collection_id: UUID
    name: str
    group_id: UUID | None


class CollectionsResponse(StrictBaseModel):
    collections: list[CollectionResponse]
    count: int | None

    _count_validator: classmethod = validators.count_validator("collections", "count")
