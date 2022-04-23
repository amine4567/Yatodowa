from typing import List

from yatodowa_api.models import Group
from yatodowa_api.sqldb import get_session


def get_groups() -> List[Group]:
    with get_session():
        groups = Group.query.all()
        return groups
