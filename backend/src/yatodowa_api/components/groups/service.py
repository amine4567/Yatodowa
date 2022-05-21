from yatodowa_api.sqldb.core import get_session
from yatodowa_api.sqldb.models import GroupTable

from .schemas import GroupResponseModel


def get_groups() -> list[GroupResponseModel]:
    with get_session():
        groups = GroupTable.query.all()

    groups_response = [GroupResponseModel(group.to_dict()) for group in groups]
    return groups_response
