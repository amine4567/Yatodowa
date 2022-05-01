from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CollectionQueryBody(BaseModel):
    name: str
    group_id: Optional[UUID]
