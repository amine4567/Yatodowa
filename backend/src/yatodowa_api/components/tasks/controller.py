from uuid import UUID

import yatodowa_api.components.tasks.service as TaskService
from yatodowa_api.components.collections.exceptions import CollectionNotFoundError
from yatodowa_api.components.tasks.exceptions import TaskNotFoundError
from yatodowa_api.consts import COMMON_API_ENDPOINT
from yatodowa_api.validation import APICallError, ErrorType, ValidatedBlueprint

from .schemas import TaskQueryArgs, TaskQueryBody, TasksResponse

tasks_api = ValidatedBlueprint("tasks_api", __name__)


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks", methods=["GET"])
def get_tasks(request_args: TaskQueryArgs):
    print(request_args)
    tasks_response = TaskService.get_tasks()
    return TasksResponse(tasks=tasks_response), 200


@tasks_api.route(COMMON_API_ENDPOINT + "/tasks", methods=["POST"])
def add_task(request_body: TaskQueryBody):
    try:
        task_response = TaskService.add_task(request_body)
    except CollectionNotFoundError as e:
        return APICallError(type=ErrorType.GENERIC, message=str(e)), 400
    else:
        return task_response, 201


@tasks_api.route(
    COMMON_API_ENDPOINT + "/tasks/<task_id>",
    methods=["DELETE"],
)
def delete_task(task_id: UUID):
    try:
        deleted_task = TaskService.delete_task(task_id)
    except TaskNotFoundError as e:
        return APICallError(type=ErrorType.GENERIC, message=str(e)), 400
    else:
        return deleted_task, 200
