# app/schemas/user.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LotoDrawBase(BaseModel):
    number_1: int
    number_2: int
    number_3: int
    number_4: int
    number_5: int
    lucky_number: Optional[int] = None

class LotoDrawCreate(LotoDrawBase):
    pass

class LotoDraw(LotoDrawBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2 (remplace orm_mode=True)
