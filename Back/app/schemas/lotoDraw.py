# app/schemas/user.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LotoDrawCreate(BaseModel):
    number_1: int
    number_2: int
    number_3: int
    number_4: int
    number_5: int
    lucky_number: Optional[int] = None

class LotoDraw(LotoDrawCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
