from datetime import datetime
from typing import Optional
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from ..dao.base import BaseDAO
from ..models.promocode import Promocode, PromocodeType


class PromocodeDAO(BaseDAO[Promocode]):
    def __init__(self, session: AsyncSession):
        super().__init__(Promocode, session)

    async def get_active_promocodes(
        self, type: Optional[PromocodeType] = None
    ) -> list[Promocode]:
        query = select(Promocode).where(
            and_(
                Promocode.date_start <= datetime.now(),
                datetime.now() <= Promocode.date_end,
            )
        )

        if type is not None:
            query = query.where(Promocode.type == type)

        result = await self._session.execute(query)
        return list(result.scalars().all())
