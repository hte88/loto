from sqlalchemy.orm import Session
from app.models.lotoDraw import LotoDraw
from app.schemas.lotoDraw import LotoDrawCreate

def create_loto_draw(db: Session, draw: LotoDrawCreate):
    db_draw = LotoDraw(**draw.model_dump())
    db.add(db_draw)
    db.commit()
    db.refresh(db_draw)
    return db_draw

def get_loto_draws(db: Session, skip: int = 0, limit: int = 100):
    return db.query(LotoDraw).offset(skip).limit(limit).all()

def get_loto_draw(db: Session, draw_id: int):
    return db.query(LotoDraw).filter(LotoDraw.id == draw_id).first()

def delete_loto_draw(db: Session, draw_id: int):
    db_draw = db.query(LotoDraw).filter(LotoDraw.id == draw_id).first()
    if db_draw:
        db.delete(db_draw)
        db.commit()
    return db_draw
