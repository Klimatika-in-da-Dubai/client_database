from datetime import datetime
from enum import IntEnum, auto
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class PromocodeType(IntEnum):
    REGISTRATION = auto()


class Promocode(Base):
    __tablename__ = "promocodes"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[int]
    type: Mapped[PromocodeType]
    date_creation: Mapped[datetime] = mapped_column(default=datetime.now)
    date_start: Mapped[datetime] = mapped_column(default=datetime.now)
    date_end: Mapped[datetime]
