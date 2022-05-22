from uuid import UUID

from pydantic import root_validator
from yatodowa_api.sqldb.consts import TASK_TEXT_MAX_LEN
from yatodowa_api.validation import StrictBaseModel, validators


class TaskPostQueryBodyModel(StrictBaseModel):
    text: str
    collection_id: UUID

    _validate_text_length: classmethod = validators.validate_text_length(
        TASK_TEXT_MAX_LEN, "text"
    )


class TaskGetQueryArgsModel(StrictBaseModel):
    page_size: int = 100
    skip: int = 0
    collection_id: UUID | None


class TaskPutQueryBodyModel(StrictBaseModel):
    text: str | None
    completed: bool | None
    collection_id: UUID | None

    _validate_text_length: classmethod = validators.validate_text_length(
        TASK_TEXT_MAX_LEN, "text"
    )

    @root_validator(pre=True)
    def validate_not_all_none(cls, values):
        if len(values) == 0:
            raise ValueError(
                "The request body is empty. At least one non empty field is needed. "
                f"Accepted fields: {list(cls.__fields__.keys())}"
            )
        return values


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

    _validate_count: classmethod = validators.validate_count("tasks", "count")
