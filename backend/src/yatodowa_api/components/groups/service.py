from typing import List

from yatodowa_api.sqldb.core import get_session
from yatodowa_api.sqldb.models import GroupTable


def get_groups() -> List[GroupTable]:
    with get_session():
        groups = GroupTable.query.all()
        return groups
