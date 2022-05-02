from typing import Optional
from uuid import UUID

from yatodowa_api.common.schemas import CustomBaseModel


class CollectionQueryBody(CustomBaseModel):
    name: str
    group_id: Optional[UUID]
