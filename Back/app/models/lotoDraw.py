# app/models/user.py
from sqlalchemy import Column, Integer, DateTime, func, UniqueConstraint
from app.database import Base

class LotoDraw(Base):
    __tablename__ = "loto_draws"

    id = Column(Integer, autoincrement=True, unique=True, index=True, nullable=False, primary_key=True)

    number_1 = Column(Integer, nullable=False)
    number_2 = Column(Integer, nullable=False)
    number_3 = Column(Integer, nullable=False)
    number_4 = Column(Integer, nullable=False)
    number_5 = Column(Integer, nullable=False)
    lucky_number = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            'number_1', 'number_2', 'number_3', 'number_4', 'number_5', 'lucky_number',
            name='unique_draw_combination'
        ),
    )
