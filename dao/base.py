from typing import Any, Optional, TypeVar, Type, Generic

from sqlalchemy import delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..base import Base

Model = TypeVar("Model", Base, Base)


class BaseDAO(Generic[Model]):
    """ORM queries for abstract table"""

    def __init__(self, model: Type[Model], session: AsyncSession):
        """
        :param model:
        :param session:
        """

        self._model = model
        self._session = session

    async def add(self, model: Model):
        await self._session.merge(model)
        await self.commit()

    async def get_all(self) -> list[Model]:
        """
        :return: List of models.
        """

        result = await self._session.execute(select(self._model))
        return list(result.scalars().all())

    async def get_by_id(self, id_: Any) -> Optional[Model]:
        """
        :param id_: input id
        :return:
        """
        result = await self._session.execute(
            select(self._model).where(self._model.id == id_)
        )
        return result.scalar_one_or_none()

    async def delete_all(self) -> None:
        """
        Clear table
        :return:
        """

        await self._session.execute(delete(self._model))

    async def count(self) -> int:
        """
        :return: count of model.
        """

        result = await self._session.execute(select(func.count(self._model.id)))
        return result.scalar_one()

    async def commit(self) -> None:
        """
        Commit re-impl
        :return:
        """

        await self._session.commit()
