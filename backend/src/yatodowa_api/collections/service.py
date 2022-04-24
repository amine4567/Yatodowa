from typing import List

from yatodowa_api.models import Collection
from yatodowa_api.sqldb import get_session


def get_collections() -> List[Collection]:
    with get_session():
        collections = Collection.query.all()
        return collections


def add_collection(name: str, group_id: str = None) -> Collection:
    with get_session() as session:
        new_collection = Collection(name=name, group_id=group_id)
        session.add(new_collection)
        return new_collection
