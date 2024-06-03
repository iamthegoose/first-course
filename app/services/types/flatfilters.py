from pydantic import BaseModel
from typing import Optional


class FlatFilters(BaseModel):
    area_from: Optional[int] = None
    area_to: Optional[int] = None
    price_from: Optional[int] = None
    price_to: Optional[int] = None
    rooms: Optional[int] = None
