from sqlalchemy.orm import Session
from app.models.lotoDraw import LotoDraw
from app.schemas.lotoDraw import LotoDrawCreate

from collections import Counter

def create_loto_draw(db: Session, draw: LotoDrawCreate):
    existing = db.query(LotoDraw).filter_by(
        number_1=draw.number_1,
        number_2=draw.number_2,
        number_3=draw.number_3,
        number_4=draw.number_4,
        number_5=draw.number_5,
        lucky_number=draw.lucky_number
    ).first()

    if existing:
        return existing

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

## start algo

def get_global_number_frequency(db: Session):
    draws = db.query(LotoDraw).all()

    counter = Counter()
    for draw in draws:
        numbers = [
            draw.number_1,
            draw.number_2,
            draw.number_3,
            draw.number_4,
            draw.number_5
        ]
        counter.update(numbers)
        if draw.lucky_number is not None:
            counter[draw.lucky_number] += 1

    frequency = [
        {"number": number, "count": count}
        for number, count in counter.most_common()
    ]

    return {
        "total_draws": len(draws),
        "global_frequency": frequency
    }
