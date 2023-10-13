from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class CommandUsage(Base):
    __tablename__ = "command_usages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    usage_timestamp: Mapped[datetime] = mapped_column(default=datetime.now)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    command: Mapped[str]
