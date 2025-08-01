# app/schemas/lotoDraw.py
from pydantic import RootModel, field_validator
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel


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


# ✅ Bulk schema compatible avec Pydantic v2
class BulkLotoDraws(RootModel[Dict[str, List[Optional[int]]]]):
    @field_validator("root")
    @classmethod
    def normalize_draws(cls, values: Dict[str, List[Optional[int]]]) -> Dict[str, List[Optional[int]]]:
        for key, draw in values.items():
            if not isinstance(draw, list):
                raise ValueError(f"Tirage {key} doit être une liste.")
            if len(draw) == 5:
                draw.append(None)  # ✅ Complète lucky_number manquant
            if len(draw) != 6:
                raise ValueError(f"Tirage {key} doit contenir exactement 5 ou 6 éléments.")
        return values


class GridGenerationConfig(BaseModel):
    shouldBalanceEvenOdd: bool = True
    favorEven: int = 50  # entre 0 et 100

    shouldBalanceHighLow: bool = True
    favorHigh: int = 50  # entre 0 et 100

    gridsToGenerate: int = 1

    shouldAvoidLogicalSequences: bool = True
    sequenceTolerance: int = 10  # % (ex: max 1 suite sur 5)

    shouldAvoidRoundNumbers: bool = True
    roundNumberTolerance: int = 50  # % (ex: max 2/5)

    includeNumbers: List[int] = []
    excludeNumbers: List[int] = []

    shouldCheckExistence: bool = False
    shouldEvaluateScore: bool = False

    shouldGenerateLucky: bool = True
    favorLucky: Optional[int] = None
    excludeLucky: List[int] = []
    # Pondération générale si besoin
    favoriserFrequence: int = 100  # 0 à 100 : 100 = favorise les plus fréquents
