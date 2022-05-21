from uuid import UUID

from yatodowa_api.validation import StrictBaseModel, validators


class TaskPostQueryBodyModel(StrictBaseModel):
    text: str
    collection_id: UUID


class TaskGetQueryArgsModel(StrictBaseModel):
    page_size: int = 100
    skip: int = 0
    collection_id: UUID | None


class TaskRespModel(StrictBaseModel):
    task_id: UUID
    text: str
    completed: bool
    collection_id: UUID


class MultiTasksRespModel(StrictBaseModel):
    tasks: list[TaskRespModel]
    total_count: int
    page_size: int
    skip: int
    count: int | None

    _count_validator: classmethod = validators.count_validator("tasks", "count")
