from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.message import File, Message, MessageFile
from ..dao.base import BaseDAO
from ..models.feedback import Feedback, FeedbackMessage


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
