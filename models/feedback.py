from datetime import datetime
from sqlalchemy import ARRAY, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    washing_id: Mapped[int] = mapped_column(ForeignKey("washings.id"))
    date: Mapped[datetime] = mapped_column(default=datetime.now)
    text: Mapped[str] = mapped_column(nullable=True)
    attached_files: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
