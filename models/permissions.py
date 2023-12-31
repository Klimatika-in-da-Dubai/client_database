from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class Permission(Base):
    """Implements permissions of the roles"""

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
