from typing import Optional
from uuid import UUID

from yatodowa_api.common.schemas import StrictBaseModel


class TaskQueryBody(StrictBaseModel):
    text: str
    collection_id: UUID


class TaskQueryArgs(StrictBaseModel):
    pagination: Optional[int]
    skip: Optional[int]
    collection_id: Optional[UUID]


class TaskResponse(StrictBaseModel):
    task_id: UUID
    text: str
    completed: bool
    collection_id: UUID
