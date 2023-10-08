from sqlalchemy.ext.asyncio import AsyncSession
from base import BaseDAO
from ..models.washing import Washing


class WashingDAO(BaseDAO[Washing]):
    """ORM queries for washings table"""

    def __init__(self, session: AsyncSession):
        super().__init__(Washing, session)
