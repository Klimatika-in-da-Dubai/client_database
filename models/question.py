from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str]
    description: Mapped[str] = mapped_column(default="")
    disabled: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return (
            f"Question(id={self.id}, text={self.text},"
            f"description={self.description}, disabled={self.disabled})"
        )


class QuestionCategory(Base):
    __tablename__ = "question_categories"

    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id"), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True
    )


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
