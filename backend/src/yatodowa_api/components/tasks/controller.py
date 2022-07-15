from uuid import UUID

import yatodowa_api.components.tasks.service as TaskService
from yatodowa_api.components.collections.exceptions import CollectionNotFoundError
from yatodowa_api.components.common.schemas import PaginationArgsModel
from yatodowa_api.components.tasks.exceptions import TaskNotFoundError
from yatodowa_api.consts import COMMON_API_PREFIX
from yatodowa_api.validation import APICallError, ErrorType, ValidatedBlueprint

from .schemas import TaskPostQueryBodyModel, TaskPutQueryBodyModel

tasks_api = ValidatedBlueprint(
    "tasks_api", __name__, url_prefix=COMMON_API_PREFIX + "/tasks"
)


@tasks_api.route("/", methods=["GET"])
def get_tasks(request_args: PaginationArgsModel):
    tasks = TaskService.get_tasks(
        page_size=request_args.page_size, skip=request_args.skip
    )
    return tasks, 200


@tasks_api.route("/", methods=["POST"])
def add_task(request_body: TaskPostQueryBodyModel):
    try:
        task_response = TaskService.add_task(request_body)
    except CollectionNotFoundError as e:
        return APICallError(type=ErrorType.MISSING_RESOURCE, message=str(e)), 400
    else:
        return task_response, 201


@tasks_api.route(
    "/<task_id>",
    methods=["PUT"],
)
def update_task(request_body: TaskPutQueryBodyModel, task_id: UUID):
    try:
        updated_task = TaskService.update_task(
            task_id=task_id, request_body=request_body
        )
    except TaskNotFoundError as e:
        return APICallError(type=ErrorType.MISSING_RESOURCE, message=str(e)), 400
    except CollectionNotFoundError as e:
        return APICallError(type=ErrorType.MISSING_RESOURCE, message=str(e)), 400
    else:
        return updated_task, 200


@tasks_api.route(
    "/<task_id>",
    methods=["DELETE"],
)
def delete_task(task_id: UUID):
    try:
        deleted_task = TaskService.delete_task(task_id)
    except TaskNotFoundError as e:
        return APICallError(type=ErrorType.MISSING_RESOURCE, message=str(e)), 400
    else:
        return deleted_task, 200
