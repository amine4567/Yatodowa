from typing import List

from yatodowa_api.models import ListsGroups
from yatodowa_api.sqldb import get_session


def get_groups() -> List[ListsGroups]:
    with get_session():
        groups = ListsGroups.query.all()
        return groups
