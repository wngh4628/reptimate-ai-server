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

class MoffListSchema(Base, BaseMixin):
    __tablename__ = "moff_list"
    name = Column(Integer, nullable=True)
    moff_recommend = Column(String(length=100), nullable=True)