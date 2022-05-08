import yatodowa_api.components.groups.service as GroupService
from yatodowa_api.api_validation import ValidatedBlueprint
from yatodowa_api.consts import COMMON_API_ENDPOINT

from .schemas import GroupsResponse

groups_api = ValidatedBlueprint("groups_api", __name__)


@groups_api.route(COMMON_API_ENDPOINT + "/groups", methods=["GET"])
def get_groups():
    groups = GroupService.get_groups()
    return GroupsResponse(count=len(groups), groups=groups), 200
