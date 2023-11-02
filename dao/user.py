from datetime import datetime
from typing import Optional
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.permissions import Permission
from ..models.role import PermissionEnum, RolePermission, UserRole


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
        user: User = await self.get_by_id(user_id)
        user.phone = phone_to_text(phone)
        await self.commit()

    async def get_users_by_phone(self, phone: str) -> list[User]:
        phone = phone_to_text(phone)
        result = await self._session.execute(select(User).where(User.phone == phone))
        return list(result.scalars().all())

    async def get_user_last_visit_datetime(
        self, user: User, before: Optional[datetime] = None
    ) -> datetime | None:
        last_washing = await self.get_user_last_washing(user, before)
        if last_washing is None:
            return None

        return last_washing.date

    async def get_user_last_washing(
        self, user: User, before: Optional[datetime] = None
    ) -> Washing | None:
        query = (
            select(Washing)
            .where(Washing.phone == user.phone)
            .order_by(Washing.date.desc())
        )

        if before is not None:
            query = query.where(Washing.date < before)

        result = await self._session.execute(query)

        return result.scalar()

    async def get_users_by_permission(self, permission_name: str) -> list[User]:
        query = (
            select(User)
            .join(UserRole, User.id == UserRole.user_id)
            .join(RolePermission, UserRole.role_id == RolePermission.role_id)
            .join(Permission, RolePermission.permission_id == Permission.id)
            .where(Permission.name == permission_name)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_user_permissions(self, user_id: int) -> list[Permission]:
        query = (
            select(Permission)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .join(User, User.id == UserRole.user_id)
            .where(User.id == user_id)
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def is_user_have_permission(
        self, user_id: int, permission: PermissionEnum
    ) -> bool:
        permissions = await self.get_user_permissions(user_id)
        permissions_name = [permission.name for permission in permissions]
        return permission in permissions_name


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
