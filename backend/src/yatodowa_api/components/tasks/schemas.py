from uuid import UUID

from pydantic import validator
from yatodowa_api.sqldb.consts import TASK_TEXT_MAX_LEN
from yatodowa_api.validation import StrictBaseModel, validators


class TaskPostQueryBodyModel(StrictBaseModel):
    text: str
    collection_id: UUID

    @validator("text")
    def validate_text_length(cls, value):
        if len(value) > TASK_TEXT_MAX_LEN:
            raise ValueError(
                "Too many characters. Maximum accepted string length: "
                + str(TASK_TEXT_MAX_LEN)
            )
        return value


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
