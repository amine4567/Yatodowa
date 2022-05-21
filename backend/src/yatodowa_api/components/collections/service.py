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


def get_collection(collection_id: UUID) -> CollectionTable:
    with get_session() as session:
        query = sqlalchemy.select(CollectionTable).where(
            CollectionTable.collection_id == collection_id
        )
        try:
            collection: CollectionTable = session.execute(query).scalar_one()
        except sqlalchemy.exc.NoResultFound:
            raise CollectionNotFoundError(
                f"No collection with id={collection_id} exists."
            )
    return collection


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
