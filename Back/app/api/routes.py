from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserOut
from app.schemas.lotoDraw import LotoDrawCreate, LotoDraw
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

@router.post("/draws/", response_model=LotoDraw)
def create_draw(draw: LotoDrawCreate, db: Session = Depends(get_db)):
    return crud_loto.create_loto_draw(db, draw)

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
