from typing import Optional
from uuid import UUID

from yatodowa_api.common.schemas import CustomBaseModel


class TaskQueryBody(CustomBaseModel):
    text: str
    collection_id: UUID


class TaskQueryArgs(CustomBaseModel):
    pagination: Optional[int]
    skip: Optional[int]
    collection_id: Optional[UUID]


class TaskResponse(CustomBaseModel):
    task_id: UUID
    text: str
    completed: bool
    collection_id: UUID
