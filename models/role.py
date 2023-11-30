from enum import StrEnum
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class Role(Base):
    """Table for user roles"""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]


class UserRole(Base):
    """Table for matching roles to users"""

    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)


class RolePermission(Base):
    """Table for matching role to permissions"""

    __tablename__ = "role_permissions"

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id"), primary_key=True
    )


class PermissionEnum(StrEnum):
    GET_FEEDBACK = "GET_FEEDBACK"
    ANSWER_FEEDBACK = "ANSWER_FEEDBACK"
    CREATE_POST = "CREATE_POST"
