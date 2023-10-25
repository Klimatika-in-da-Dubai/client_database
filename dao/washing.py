from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..dao.base import BaseDAO
from ..models.washing import Washing


class WashingDAO(BaseDAO[Washing]):
    """ORM queries for washings table"""

    def __init__(self, session: AsyncSession):
        super().__init__(Washing, session)

    async def is_washing_exists(self, washing: Washing) -> bool:
        result = await self._session.execute(
            select(Washing).where(Washing.id == washing.id)
        )
        return result.first() is not None
