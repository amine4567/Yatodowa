from uuid import UUID

import yatodowa_api.components.tasks.service as TaskService
from flask import Blueprint, jsonify
from yatodowa_api.common.http_utils import validate_request_body, validate_url_vars
from yatodowa_api.components.collections.exceptions import CollectionNotFoundError
from yatodowa_api.components.tasks.exceptions import TaskNotFoundError
from yatodowa_api.consts import COMMON_API_ENDPOINT

from .schemas import TaskQuery

tasks_api = Blueprint("tasks_api", __name__)


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks", methods=["GET"])
def get_tasks():
    tasks_response = TaskService.get_tasks()
    return jsonify([elt.dict() for elt in tasks_response]), 200


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks", methods=["POST"])
@validate_request_body
def add_task(request_body: TaskQuery):
    try:
        task_response = TaskService.add_task(request_body)
    except CollectionNotFoundError as e:
        return jsonify({"error_message": str(e)}), 400
    else:
        return jsonify(task_response.dict()), 201


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks/<task_id>", methods=["DELETE"])
@validate_url_vars
def delete_task(task_id: UUID):
    try:
        deleted_task = TaskService.delete_task(task_id)
    except TaskNotFoundError as e:
        return jsonify({"error_message": str(e)}), 400
    else:
        return jsonify(deleted_task.dict()), 200
