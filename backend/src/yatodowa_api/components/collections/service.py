from typing import List

from yatodowa_api.sqldb.core import get_session
from yatodowa_api.sqldb.models import CollectionTable


def get_collections() -> List[CollectionTable]:
    with get_session():
        collections = CollectionTable.query.all()
        return collections


def add_collection(name: str, group_id: str = None) -> CollectionTable:
    with get_session() as session:
        new_collection = CollectionTable(name=name, group_id=group_id)
        session.add(new_collection)
        return new_collection
