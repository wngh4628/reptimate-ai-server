from core.database.conn import Base, db
from core.database.schema import BaseMixin
from sqlalchemy import (
    Column,
    Integer,
    String,
)

class ValueAnalyzerSchema(Base, BaseMixin):
    __tablename__ = "value_analyzer"
    user_idx = Column(Integer, nullable=True)
    pet_name = Column(String(length=100), nullable=True)
    morph = Column(String(length=100), nullable=False)
    gender = Column(String(length=100), nullable=False)
    head_score = Column(Integer, nullable=False)
    dorsal_score = Column(Integer, nullable=False)
    tail_score = Column(Integer, nullable=False)
    left_score = Column(Integer, nullable=False)
    right_score = Column(Integer, nullable=False)
    left_info = Column(String(length=1000), nullable=True)
    right_info = Column(String(length=1000), nullable=True)
    total_score = Column(Integer, nullable=True)
    top_img = Column(String(length=255), nullable=True)
    left_img = Column(String(length=255), nullable=False)
    right_img = Column(String(length=255), nullable=True)