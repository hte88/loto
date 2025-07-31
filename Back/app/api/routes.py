from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from typing import List
from app.schemas.user import UserCreate, UserOut
from app.schemas.lotoDraw import LotoDrawCreate, LotoDraw, BulkLotoDraws
from app.crud import user as crud_user
from app.crud import lotoDraw as crud_loto
from app.database import SessionLocal

router = APIRouter()

# Dépendance pour la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------- USERS ------------

@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)

@router.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return crud_user.get_users(db)

@router.get("/users/{email}", response_model=UserOut)
def get_user(email: str, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

# ----------- DRAWS (LOTO) ------------

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

    for draw in payload.root.values():  # .root car on utilise RootModel
        loto = LotoDrawCreate(
            number_1=draw[0],
            number_2=draw[1],
            number_3=draw[2],
            number_4=draw[3],
            number_5=draw[4],
            lucky_number=draw[5]  # ← None accepté ici
        )
        created = crud_loto.create_loto_draw(db, loto)
        results.append(created)

    return results

@router.get("/draws/", response_model=list[LotoDraw])
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
