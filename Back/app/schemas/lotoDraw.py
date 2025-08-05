from pydantic import RootModel, field_validator, BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class LotoDrawCreate(BaseModel):
    date_draw: datetime
    number_1: int
    number_2: int
    number_3: int
    number_4: int
    number_5: int
    number_6: Optional[int] = None
    additional_number: Optional[int] = None
    lucky_number: Optional[int] = None
    game_type: str

class LotoDraw(LotoDrawCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class BulkLotoDraws(RootModel[Dict[str, List[Optional[int]]]]):
    @field_validator("root")
    @classmethod
    def normalize_draws(cls, values):
        for key, draw in values.items():
            if not isinstance(draw, list):
                raise ValueError(f"Tirage {key} doit être une liste.")
            if len(draw) == 5:
                draw.append(None)
            if len(draw) != 6:
                raise ValueError(f"Tirage {key} doit contenir 5 ou 6 éléments.")
        return values

class GridGenerationConfig(BaseModel):
    shouldBalanceEvenOdd: bool = True
    favorEven: int = 50
    shouldBalanceHighLow: bool = True
    favorHigh: int = 50
    gridsToGenerate: int = 1
    numbersToGenerate: int = 5
    shouldAvoidLogicalSequences: bool = True
    sequenceTolerance: int = 10
    shouldAvoidRoundNumbers: bool = True
    roundNumberTolerance: int = 50
    includeNumbers: List[int] = []
    excludeNumbers: List[int] = []
    shouldCheckExistence: bool = False
    shouldEvaluateScore: bool = False
    shouldGenerateLucky: bool = True
    favorLucky: Optional[int] = None
    excludeLucky: List[int] = []
    favoriserFrequence: int = 100
    includedSources: List[str] = ["loto", "super", "grand"]
