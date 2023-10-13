from datetime import datetime
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from ..models.user import User
from ..models.washing import Washing
from ..dao.base import BaseDAO
from ..utils.phone import phone_to_text


class UserNotRegisteredError(Exception):
    def __init__(self, user_id: int) -> None:
        super().__init__(user_id)


class UserDAO(BaseDAO[User]):
    """ORM queries for users table"""

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def add_user(self, user: User) -> None:
        """
        Add user to database if not added yet. If added, tries to update parameters.
        :param user: Telegram user.
        """

        await self._session.merge(user)
        await self._session.commit()

    async def add_phone(self, user_id: int, phone: str) -> None:
        user: User | None = await self.get_by_id(user_id)
        if user is None:
            raise UserNotRegisteredError(user_id)

        user.phone = phone_to_text(phone)
        await self.commit()

    async def get_users_by_phone(self, phone: str) -> list[User]:
        phone = phone_to_text(phone)
        result = await self._session.execute(select(User).where(User.phone == phone))
        return list(result.scalars().all())

    async def get_user_last_visit(self, user: User) -> datetime | None:
        last_washing = await self.get_user_last_washing(user)
        if last_washing is None:
            return None

        return last_washing.date

    async def get_user_last_washing(self, user: User) -> Washing | None:
        if user.phone is None:
            raise ValueError("Can't get last washing of user with no phone")

        result = await self._session.execute(
            select(Washing)
            .where(Washing.phone == user.phone)
            .order_by(Washing.date.desc())
        )

        return result.scalar()


def get_user_from_message(message: Message) -> User:
    """
    Creates User model from telegram message
    """
    return User(
        id=message.from_user.id,  # pyright: ignore
        first_name=message.from_user.first_name,  # pyright: ignore
        last_name=message.from_user.last_name,  # pyright: ignore
        username=message.from_user.username,  # pyright: ignore
    )
