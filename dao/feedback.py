from datetime import datetime
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.message import File, Message, MessageFile
from ..models.question import Category, QuestionCategory
from ..models.washing import Washing
from ..dao.base import BaseDAO
from ..models.feedback import (
    ConversationStatus,
    Feedback,
    FeedbackConversation,
    FeedbackMessage,
)


class FeedbackDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Feedback, session)

    async def attach_message(self, feedback: Feedback, message: Message):
        if feedback.user_id != message.user_id:
            raise ValueError(
                "feedback and message should be connected to the same user"
            )
        feedback_message = FeedbackMessage(feedback.id, message.id, message.user_id)
        await self.add(feedback_message)

    async def attach_message_by_ids(self, feedback_id: int, message_id: int):
        feedback = await self.get_by_id(feedback_id)
        feedback_message = FeedbackMessage(
            feedback_id=feedback.id, message_id=message_id, user_id=feedback.user_id
        )
        await self.add(feedback_message)

    async def get_feedback_messages(self, feedback_id: int) -> list[Message]:
        result = await self._session.execute(
            select(Message)
            .join(FeedbackMessage, FeedbackMessage.message_id == Message.id)
            .where(FeedbackMessage.feedback_id == feedback_id)
            .order_by(Message.id.asc())
        )
        return list(result.scalars().all())

    async def get_attached_files_to_feedback(self, feedback_id: int) -> list[File]:
        query = (
            select(File)
            .join(MessageFile, MessageFile.file_id == File.id)
            .join(Message, Message.id == MessageFile.message_id)
            .join(FeedbackMessage, FeedbackMessage.message_id == Message.id)
            .where(FeedbackMessage.feedback_id == feedback_id)
            .order_by(Message.id.asc())
        )

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_feedback_messages_between_time(
        self,
        begin: datetime,
        end: datetime,
        question_category: Optional[str] = None,
    ) -> list[Message]:
        query = (
            select(Message)
            .join(FeedbackMessage, FeedbackMessage.message_id == Message.id)
            .join(Feedback, FeedbackMessage.feedback_id == Feedback.id)
            .join(
                QuestionCategory, QuestionCategory.question_id == Feedback.question_id
            )
            .join(Category, Category.id == QuestionCategory.category_id)
            .join(Washing, Washing.id == Feedback.washing_id)
            .where(Feedback.date.between(begin, end))
        )

        if question_category:
            query = query.where(Category.name == question_category)

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def create_conversation(self, feedback_id: int, reviewer_id: int):
        feedback_conversation = FeedbackConversation(
            feedback_id=feedback_id, reviewer_id=reviewer_id
        )
        await self.add(feedback_conversation)

    async def is_feedback_conversation_active(self, feedback_id: int) -> bool:
        query = select(FeedbackConversation).where(
            FeedbackConversation.feedback_id == feedback_id
        )

        result = await self._session.execute(query)
        if len(result.scalars().all()) == 0:
            return False

        return any(
            [
                conv.status == ConversationStatus.IN_PROGRESS
                for conv in result.scalars().all()
            ]
        )

    async def get_conversation(
        self, feedback_id: int, reviewer_id: int
    ) -> FeedbackConversation:
        query = (
            select(FeedbackConversation)
            .where(FeedbackConversation.feedback_id == feedback_id)
            .where(FeedbackConversation.reviewer_id == reviewer_id)
        )
        result = await self._session.execute(query)
        return result.scalar_one()

    async def update_conversation_status(
        self, feedback_id: int, reviewer_id: int, status: ConversationStatus
    ):
        feedback_conversation = await self.get_conversation(feedback_id, reviewer_id)
        feedback_conversation.status = status
        await self.commit()
