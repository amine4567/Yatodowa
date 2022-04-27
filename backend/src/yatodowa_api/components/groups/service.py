from typing import List

from yatodowa_api.sqldb.core import get_session
from yatodowa_api.sqldb.models import Group


def get_groups() -> List[Group]:
    with get_session():
        groups = Group.query.all()
        return groups
