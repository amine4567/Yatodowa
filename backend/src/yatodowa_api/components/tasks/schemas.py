from uuid import UUID

from yatodowa_api.api_validation import StrictBaseModel, validators


class TaskQueryBody(StrictBaseModel):
    text: str
    collection_id: UUID


class TaskQueryArgs(StrictBaseModel):
    pagination: int | None
    skip: int | None
    collection_id: UUID | None


class TaskResponse(StrictBaseModel):
    task_id: UUID
    text: str
    completed: bool
    collection_id: UUID


class TasksResponse(StrictBaseModel):
    tasks: list[TaskResponse]
    count: int | None

    _count_validator: classmethod = validators.count_validator("tasks", "count")
