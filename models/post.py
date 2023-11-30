from datetime import datetime
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    creation_date: Mapped[datetime] = mapped_column(default=datetime.now)
    upload_date: Mapped[datetime] = mapped_column(nullable=True)


class PostPart(Base):
    __tablename__ = "post_parts"

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    part_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str]


class PostPartFile(Base):
    __tablename__ = "post_part_files"

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    part_number: Mapped[int] = mapped_column(Integer, primary_key=True)
    file_order: Mapped[int]
    file_id: Mapped[str] = mapped_column(ForeignKey("files.id"), primary_key=True)
