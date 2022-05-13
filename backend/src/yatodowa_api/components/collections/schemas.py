from uuid import UUID

from pydantic import validator
from yatodowa_api.api_validation import StrictBaseModel


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

    @validator("count", always=True)
    def compute_count(cls, _, values: dict) -> int:
        return len(values["collections"])
