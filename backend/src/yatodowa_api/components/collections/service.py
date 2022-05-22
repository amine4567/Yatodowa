from uuid import UUID

import sqlalchemy
from yatodowa_api.sqldb.core import get_session
from yatodowa_api.sqldb.models import CollectionTable

from .exceptions import CollectionNotFoundError
from .schemas import CollectionPostQueryBodyModel, CollectionRespModel


def get_collections() -> list[CollectionRespModel]:
    with get_session():
        collections = CollectionTable.query.all()

    collections_response = [
        CollectionRespModel(**collection.to_dict()) for collection in collections
    ]
    return collections_response


def check_if_collection_exists(collection_id: UUID) -> bool:
    with get_session() as session:
        collection = session.get(CollectionTable, collection_id)
        if collection is None:
            raise CollectionNotFoundError(
                f"No collection with id={collection_id} exists."
            )
        else:
            return True


def add_collection(
    collection_query: CollectionPostQueryBodyModel,
) -> CollectionRespModel:
    with get_session() as session:
        new_collection = CollectionTable(
            name=collection_query.name, group_id=collection_query.group_id
        )
        session.add(new_collection)

    collection_response = CollectionRespModel(**new_collection.to_dict())
    return collection_response
