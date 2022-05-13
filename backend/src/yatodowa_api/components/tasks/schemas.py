from uuid import UUID

from pydantic import validator
from yatodowa_api.api_validation import StrictBaseModel


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

    @validator("count", always=True)
    def compute_count(cls, _, values: dict) -> int:
        return len(values["tasks"])
