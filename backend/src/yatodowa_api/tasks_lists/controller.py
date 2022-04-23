import yatodowa_api.tasks_lists.service as TasksListService
from flask import Blueprint, jsonify, request
from yatodowa_api.consts import COMMON_API_ENDPOINT

tasks_lists_api = Blueprint("tasks_lists_api", __name__)


@tasks_lists_api.route(COMMON_API_ENDPOINT + "/lists", methods=["GET"])
def get_lists():
    tasks_lists = TasksListService.get_lists()
    return jsonify([elt.to_dict() for elt in tasks_lists]), 200


@tasks_lists_api.route(COMMON_API_ENDPOINT + "/lists", methods=["POST"])
def add_list():
    request_body = request.get_json()
    mandatory_fields = set(["list_name"])

    try:
        missing_fields = mandatory_fields - set(request_body.keys())
        assert len(missing_fields) == 0
    except AssertionError:
        return (
            jsonify(
                {
                    "error": "The following mandatory fields are missing: "
                    + str(missing_fields)
                }
            ),
            400,
        )

    existing_list_names = [elt.list_name for elt in TasksListService.get_lists()]
    try:
        assert request_body["list_name"] not in existing_list_names
    except AssertionError:
        return (
            jsonify(
                {
                    "error": "There already exist a tasks list with the name "
                    + request_body["list_name"]
                }
            ),
            400,
        )

    task = TasksListService.add_list(
        list_name=request_body["list_name"],
        group_name=request_body.get("group_name", None),
    )

    return (
        jsonify(
            {
                "result": "A new tasks list was created successfully.",
                "description": task.to_dict(),
            }
        ),
        201,
    )
