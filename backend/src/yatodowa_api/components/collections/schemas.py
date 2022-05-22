from uuid import UUID

from yatodowa_api.validation import StrictBaseModel, validators


class CollectionPostQueryBodyModel(StrictBaseModel):
    name: str
    group_id: UUID | None


class CollectionRespModel(StrictBaseModel):
    collection_id: UUID
    name: str
    group_id: UUID | None


class MultiCollectionsRespModel(StrictBaseModel):
    collections: list[CollectionRespModel]
    count: int | None

    _validate_count: classmethod = validators.validate_count("collections", "count")
