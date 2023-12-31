from datetime import datetime
from sqlalchemy import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class Washing(Base):
    __tablename__ = "washings"

    id: Mapped[str] = mapped_column(primary_key=True)
    terminal: Mapped[int]
    date: Mapped[datetime]
    state: Mapped[str]
    start_date: Mapped[datetime] = mapped_column(nullable=True)
    end_date: Mapped[datetime] = mapped_column(nullable=True)
    mode: Mapped[int]
    phone: Mapped[str] = mapped_column(VARCHAR(12), nullable=True)
    bonuses: Mapped[int] = mapped_column(nullable=True)
    promocode: Mapped[int] = mapped_column(nullable=True)
    price: Mapped[float]

    def __repr__(self) -> str:
        return str(self.__dict__)
