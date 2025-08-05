from sqlalchemy import Column, Integer, DateTime, func, String, UniqueConstraint
from app.database import Base

class Loto(Base):
    __tablename__ = "loto_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_draw = Column(DateTime, nullable=False)
    number_1 = Column(Integer, nullable=False)
    number_2 = Column(Integer, nullable=False)
    number_3 = Column(Integer, nullable=False)
    number_4 = Column(Integer, nullable=False)
    number_5 = Column(Integer, nullable=False)
    number_6 = Column(Integer, nullable=True)
    additional_number = Column(Integer, nullable=True)
    lucky_number = Column(Integer, nullable=True)
    game_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("date_draw", "number_1", "number_2", "number_3", "number_4", "number_5", "number_6", "additional_number", "lucky_number", "game_type", name="unique_draw_combination"),
    )

class SuperLoto(Base):
    __tablename__ = "super_loto_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_draw = Column(DateTime, nullable=False)
    number_1 = Column(Integer, nullable=False)
    number_2 = Column(Integer, nullable=False)
    number_3 = Column(Integer, nullable=False)
    number_4 = Column(Integer, nullable=False)
    number_5 = Column(Integer, nullable=False)
    number_6 = Column(Integer, nullable=True)
    additional_number = Column(Integer, nullable=True)
    lucky_number = Column(Integer, nullable=True)
    game_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("date_draw", "number_1", "number_2", "number_3", "number_4", "number_5", "number_6", "additional_number", "lucky_number", "game_type", name="unique_draw_combination"),
    )

class GrandLoto(Base):
    __tablename__ = "grand_loto_results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_draw = Column(DateTime, nullable=False)
    number_1 = Column(Integer, nullable=False)
    number_2 = Column(Integer, nullable=False)
    number_3 = Column(Integer, nullable=False)
    number_4 = Column(Integer, nullable=False)
    number_5 = Column(Integer, nullable=False)
    number_6 = Column(Integer, nullable=True)
    additional_number = Column(Integer, nullable=True)
    lucky_number = Column(Integer, nullable=True)
    game_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("date_draw", "number_1", "number_2", "number_3", "number_4", "number_5", "number_6", "additional_number", "lucky_number", "game_type", name="unique_draw_combination"),
    )
