from sqlalchemy.ext.asyncio import AsyncSession
from ..dao.base import BaseDAO
from ..models.feedback import Feedback


class FeedbackDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Feedback, session)
