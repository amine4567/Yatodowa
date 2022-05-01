from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TaskQueryBody(BaseModel):
    text: str
    collection_id: UUID


class TaskQueryArgs(BaseModel):
    pagination: Optional[int]
    skip: Optional[int]
    collection_id: Optional[UUID]


class TaskResponse(BaseModel):
    task_id: UUID
    text: str
    completed: bool
    collection_id: UUID
