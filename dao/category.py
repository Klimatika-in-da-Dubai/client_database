from sqlalchemy.ext.asyncio import AsyncSession
from ..dao.base import BaseDAO
from ..models.question import Category


class CategoryDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)
