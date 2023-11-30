from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.message import File
from ..dao.base import BaseDAO
from ..models.post import Post, PostPart, PostPartFile


class PostDAO(BaseDAO):
    def __init__(self, session: AsyncSession):
        super().__init__(Post, session)

    async def get_post_part(self, post_id: int, part_number: int) -> PostPart:
        query = (
            select(PostPart)
            .where(PostPart.post_id == post_id)
            .where(PostPart.part_number == part_number)
        )
        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_post_parts(self, post_id: int) -> list[PostPart]:
        query = (
            select(PostPart)
            .where(PostPart.post_id == post_id)
            .order_by(PostPart.part_number)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_post_part_attached_files(
        self, post_id: int, part_number: int
    ) -> list[File]:
        query = (
            select(File)
            .join(PostPartFile, PostPartFile.file_id == File.id)
            .where(PostPartFile.post_id == post_id)
            .where(PostPartFile.part_number == part_number)
            .order_by(PostPartFile.file_order)
        )

        result = await self._session.execute(query)
        return list(result.scalars().all())
