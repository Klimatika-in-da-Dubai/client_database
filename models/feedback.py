from datetime import datetime
from enum import Enum, auto
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    washing_id: Mapped[int] = mapped_column(ForeignKey("washings.id"))
    date: Mapped[datetime] = mapped_column(default=datetime.now)


class FeedbackMessage(Base):
    """
    feedback_id: ForeignKey("feedbacks.id"), primary_key=True
    message_id: ForeignKey("messages.id"), primary_key=True
    user_id: ForeignKey("users.id"), primary_key=True
    """

    __tablename__ = "feedback_messages"

    feedback_id: Mapped[int] = mapped_column(
        ForeignKey("feedbacks.id"), primary_key=True
    )
    message_id: Mapped[int] = mapped_column(ForeignKey("messages.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class ConversationStatus(Enum):
    IN_PROGRESS = auto()
    CLOSED = auto()
    CANCELED = auto()


class FeedbackConversation(Base):
    __tablename__ = "feedback_conversations"

    feedback_id: Mapped[int] = mapped_column(
        ForeignKey("feedbacks.id", ondelete="CASCADE"), primary_key=True
    )
    reviewer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    status: Mapped[ConversationStatus] = mapped_column(
        default=ConversationStatus.IN_PROGRESS
    )
