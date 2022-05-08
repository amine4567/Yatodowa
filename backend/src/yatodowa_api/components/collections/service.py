from yatodowa_api.sqldb.core import get_session
from yatodowa_api.sqldb.models import CollectionTable

from .schemas import CollectionQueryBody, CollectionResponse


def get_collections() -> list[CollectionResponse]:
    with get_session():
        collections = CollectionTable.query.all()

    collections_response = [
        CollectionResponse(**collection.to_dict()) for collection in collections
    ]
    return collections_response


def add_collection(collection_query: CollectionQueryBody) -> CollectionResponse:
    with get_session() as session:
        new_collection = CollectionTable(
            name=collection_query.name, group_id=collection_query.group_id
        )
        session.add(new_collection)

    collection_response = CollectionResponse(**new_collection.to_dict())
    return collection_response
