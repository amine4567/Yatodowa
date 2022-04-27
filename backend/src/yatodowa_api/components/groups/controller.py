import yatodowa_api.components.groups.service as GroupService
from flask import Blueprint, jsonify
from yatodowa_api.consts import COMMON_API_ENDPOINT

groups_api = Blueprint("groups_api", __name__)


@groups_api.route(COMMON_API_ENDPOINT + "/groups", methods=["GET"])
def get_groups():
    groups = GroupService.get_groups()
    return jsonify([group.name for group in groups]), 200
