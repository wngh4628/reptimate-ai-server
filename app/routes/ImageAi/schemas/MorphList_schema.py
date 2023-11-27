from core.database.conn import Base, db
from core.database.schema import BaseMixin
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func,
    Enum,
    Boolean,
    ForeignKey,
)

class MorphListSchema(Base, BaseMixin):
    __tablename__ = "morph_list"
    name = Column(Integer, nullable=True)
    morph_recommend = Column(String(length=100), nullable=True)