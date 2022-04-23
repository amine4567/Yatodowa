from uuid import UUID

import yatodowa_api.tasks.service as TaskService
from flask import Blueprint, jsonify, request
from yatodowa_api.consts import COMMON_API_ENDPOINT

tasks_api = Blueprint("tasks_api", __name__)


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks", methods=["GET"])
def get_tasks():
    tasks = TaskService.get_tasks()
    return jsonify([elt.to_dict() for elt in tasks]), 200


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks", methods=["POST"])
def add_task():
    request_body = request.get_json()
    mandatory_fields = set(["text", "list_name"])

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

    task = TaskService.add_task(
        text=request_body["text"], list_name=request_body["list_name"]
    )

    return (
        jsonify(
            {
                "result": "A new task was created successfully.",
                "description": task.to_dict(),
            }
        ),
        201,
    )


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id: str):
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        return (
            jsonify({"error_message": f"{task_id} is not a valid hex UUID string"}),
            400,
        )

    try:
        TaskService.delete_task(task_uuid)
    except ValueError as e:
        return jsonify({"error_message": str(e)}), 400

    return jsonify({"result": f"task with id {task_uuid} deleted successfully"}), 200
