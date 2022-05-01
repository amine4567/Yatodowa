from uuid import UUID

from pydantic import BaseModel


class TaskQuery(BaseModel):
    text: str
    collection_id: UUID


class TaskResponse(BaseModel):
    task_id: UUID
    text: str
    completed: bool
    collection_id: UUID
