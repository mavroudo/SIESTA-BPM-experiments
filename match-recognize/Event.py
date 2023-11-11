from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    activity: Mapped[str] = mapped_column(String(50))
    case_id: Mapped[str] = mapped_column(String(100))
    timestamp: Mapped[str] = mapped_column(String(100))


class EventEntryBase(BaseModel):
    id: int
    activity: str
    case_id: str
    timestamp: str

    class Config:
        from_attributes = True
