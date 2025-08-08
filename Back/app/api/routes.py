from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserCreate, UserOut
from app.schemas.lotoDraw import LotoDrawCreate, LotoDraw, BulkLotoDraws, GridGenerationConfig
from app.crud import user as crud_user
from app.crud import lotoDraw as crud_loto
from app.database import SessionLocal
from datetime import datetime

router = APIRouter()

# ---------- DB ----------

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- USERS ----------

@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.get("/users/{email}", response_model=UserOut)
def get_user(email: str, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

# ---------- STATS ----------

@router.get("/draws/weights")
def get_weighted_stats(
    sources: str = "loto,super,grand",
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    db: Session = Depends(get_db)
):
    try:
        sources_list = [s.strip().lower() for s in sources.split(",") if s.strip()]
        return crud_loto.get_weighted_numbers_combined(db, sources=sources_list, start_date=start_date, end_date=end_date)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ---------- GENERATION ----------

@router.post("/draws/generate")
def generate_draws(config: GridGenerationConfig, db: Session = Depends(get_db)):
    try:
        return crud_loto.generate_weighted_grids(db, config.model_dump())
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



# ---------- DRAWS ----------

@router.post("/draws/", response_model=List[LotoDraw])
def create_draws(draws: List[LotoDrawCreate], db: Session = Depends(get_db)):
    created_draws = []
    for draw in draws:
        created = crud_loto.create_loto_draw(db, draw)
        created_draws.append(created)
    return created_draws

@router.post("/draws/bulk", response_model=List[LotoDraw])
def create_draws_bulk(payload: BulkLotoDraws, db: Session = Depends(get_db)):
    results = []
    for draw in payload.root.values():
        loto = LotoDrawCreate(
            date_draw=None,  # à ajuster selon les besoins
            number_1=draw[0],
            number_2=draw[1],
            number_3=draw[2],
            number_4=draw[3],
            number_5=draw[4],
            additional_number=draw[5],
            lucky_number=draw[6],
            game_type="loto",  # ou à passer dynamiquement
        )
        created = crud_loto.create_loto_draw(db, loto)
        results.append(created)
    return results

@router.get("/draws", response_model=List[LotoDraw])
def read_draws(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_loto.get_loto_draws(db, skip=skip, limit=limit)

@router.get("/draws/{draw_id}", response_model=LotoDraw)
def read_draw(draw_id: int, db: Session = Depends(get_db)):
    db_draw = crud_loto.get_loto_draw(db, draw_id)
    if db_draw is None:
        raise HTTPException(status_code=404, detail="Tirage non trouvé")
    return db_draw

@router.delete("/draws/{draw_id}", response_model=LotoDraw)
def delete_draw(draw_id: int, db: Session = Depends(get_db)):
    db_draw = crud_loto.delete_loto_draw(db, draw_id)
    if db_draw is None:
        raise HTTPException(status_code=404, detail="Tirage non trouvé")
    return db_draw
