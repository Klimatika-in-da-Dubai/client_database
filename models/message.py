from aiogram.enums import InputMediaType
from apscheduler.executors.base import datetime
from sqlalchemy import VARCHAR, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class Message(Base):
    """
    id: Mapped[int]
    user_id: Mapped[int] ForeignKey("users.id")
    date: Mapped[datetime] default=datetime.now
    text: Mapped[str] default=""

    """

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date: Mapped[datetime] = mapped_column(default=datetime.now)
    text: Mapped[str] = mapped_column(default="")


class MessageFile(Base):
    __tablename__ = "message_files"

    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"), primary_key=True)
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id"), primary_key=True)


class File(Base):
    __tablename__ = "files"

    id: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[InputMediaType]
    caption: Mapped[str] = mapped_column(VARCHAR(1024), default="")
