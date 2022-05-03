from typing import Optional
from uuid import UUID

from yatodowa_api.common.schemas import StrictBaseModel


class CollectionQueryBody(StrictBaseModel):
    name: str
    group_id: Optional[UUID]
