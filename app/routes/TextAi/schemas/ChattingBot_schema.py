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

class ChattingBotSchema(Base, BaseMixin):
    __tablename__ = "chatting_bot"
    categorey = Column(String(length=100), nullable=True)
    document = Column(String(length=5000), nullable=True)
