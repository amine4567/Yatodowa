import yatodowa_api.components.groups.service as GroupService
from yatodowa_api.consts import COMMON_API_PREFIX
from yatodowa_api.validation import ValidatedBlueprint

from .schemas import MultiGroupsResponseModel

groups_api = ValidatedBlueprint(
    "groups_api", __name__, url_prefix=COMMON_API_PREFIX + "/groups"
)


@groups_api.route("/", methods=["GET"])
def get_groups():
    groups = GroupService.get_groups()
    return MultiGroupsResponseModel(groups=groups), 200
