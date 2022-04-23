from uuid import UUID

import yatodowa_api.tasks.service as TaskService
from flask import Blueprint, jsonify, request
from yatodowa_api.collections.exceptions import CollectionNotFoundError
from yatodowa_api.consts import COMMON_API_ENDPOINT
from yatodowa_api.tasks.exceptions import TaskNotFoundError

tasks_api = Blueprint("tasks_api", __name__)


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks", methods=["GET"])
def get_tasks():
    tasks = TaskService.get_tasks()
    return jsonify([elt.to_dict() for elt in tasks]), 200


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks", methods=["POST"])
def add_task():
    request_body = request.get_json()

    # Check for missing fields in the call
    mandatory_fields = set(["text", "collection_name"])
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

    # Try to call the add task service function
    try:
        task = TaskService.add_task(
            text=request_body["text"], collection_name=request_body["collection_name"]
        )
    except CollectionNotFoundError as e:
        return jsonify({"error_message": str(e)}), 400
    else:
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
    # Check is task_id is a valid UUID string
    try:
        task_uuid = UUID(task_id)
    except ValueError:
        return (
            jsonify({"error_message": f"{task_id} is not a valid hex UUID string"}),
            400,
        )

    # Try to call the delete task service function
    try:
        deleted_task = TaskService.delete_task(task_uuid)
    except TaskNotFoundError as e:
        return jsonify({"error_message": str(e)}), 400
    else:
        return (
            jsonify(
                {
                    "result": f"task with id {task_uuid} deleted successfully",
                    "description": deleted_task.to_dict(),
                }
            ),
            200,
        )
