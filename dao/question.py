from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..dao.base import BaseDAO
from ..models.question import Category, CategoryEnum, Question, QuestionCategory


class QuestionDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Question, session)

    async def get_active_questions(
        self, category: Optional[CategoryEnum] = None
    ) -> list[Question]:
        query = select(self._model)
        if category is not None:
            query = (
                query.join(
                    QuestionCategory, QuestionCategory.question_id == Question.id
                )
                .join(Category, Category.id == QuestionCategory.category_id)
                .where(Category.name == category)
            )

        query = query.where(self._model.disabled.is_(False))

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_question_categories(self, question_id: int) -> list[Category]:
        result = await self._session.execute(
            select(Category)
            .join(QuestionCategory, QuestionCategory.category_id == Category.id)
            .where(QuestionCategory.question_id == question_id)
        )
        return list(result.scalars().all())

    async def is_question_have_category(
        self, question_id: int, category: CategoryEnum
    ) -> bool:
        query = (
            select(Question)
            .join(QuestionCategory, QuestionCategory.question_id == question_id)
            .join(Category, Category.id == QuestionCategory.category_id)
            .where(Category.name == category)
            .where(Question.id == question_id)
        )
        result = await self._session.execute(query)
        print(result)
        return result.scalar_one_or_none() is not None
