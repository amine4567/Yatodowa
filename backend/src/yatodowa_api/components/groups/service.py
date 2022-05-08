from yatodowa_api.sqldb.core import get_session
from yatodowa_api.sqldb.models import GroupTable

from .schemas import GroupResponse


def get_groups() -> list[GroupResponse]:
    with get_session():
        groups = GroupTable.query.all()

    groups_response = [GroupResponse(group.to_dict()) for group in groups]
    return groups_response
