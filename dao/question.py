from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..dao.base import BaseDAO
from ..models.question import Question, QuestionCategory


class QuestionDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Question, session)

    async def get_questions_by_category_id(self, category_id: int) -> list[Question]:
        result = await self._session.execute(
            select(self._model)
            .join(QuestionCategory, QuestionCategory.category_id == category_id)
            .where(self._model.disabled.is_(False))
        )
        return list(result.scalars().all())
