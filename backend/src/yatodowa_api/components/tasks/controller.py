from uuid import UUID

import yatodowa_api.components.tasks.service as TaskService
from flask import Blueprint, jsonify
from yatodowa_api.common.http_utils import validate_request, validate_uuid_input
from yatodowa_api.components.collections.exceptions import CollectionNotFoundError
from yatodowa_api.components.tasks.exceptions import TaskNotFoundError
from yatodowa_api.consts import COMMON_API_ENDPOINT

from .schemas import TaskQuery, TaskResponse

tasks_api = Blueprint("tasks_api", __name__)


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks", methods=["GET"])
def get_tasks():
    tasks = TaskService.get_tasks()
    return jsonify([elt.to_dict() for elt in tasks]), 200


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks", methods=["POST"])
@validate_request
def add_task(request_body: TaskQuery) -> TaskResponse:
    try:
        task = TaskService.add_task(request_body)
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
@validate_uuid_input("task_id")
def delete_task(task_id: UUID):
    try:
        deleted_task = TaskService.delete_task(task_id)
    except TaskNotFoundError as e:
        return jsonify({"error_message": str(e)}), 400
    else:
        return (
            jsonify(
                {
                    "result": f"task with id {task_id} deleted successfully",
                    "description": deleted_task.to_dict(),
                }
            ),
            200,
        )
