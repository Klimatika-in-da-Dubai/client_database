from sqlalchemy.ext.asyncio import AsyncSession
from ..dao.base import BaseDAO
from ..models.message import File


class FileDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(File, session)
