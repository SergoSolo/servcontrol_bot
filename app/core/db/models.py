from datetime import datetime

from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship

from app.core.constants import UserRoleConstant
from app.core.db.db import Base


def fresh_timestamp() -> datetime:
    """Временная метка."""
    return datetime.utcnow


class BaseModel(Base):
    """Абстрактная модель с общими полями."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=fresh_timestamp())
    updated_at = Column(DateTime, onupdate=fresh_timestamp())


class User(BaseModel):
    """Модель пользователя."""

    __tablename__ = "users"

    first_name = Column(String(150))
    last_name = Column(String(150))
    town = Column(String(150))
    telegram_id = Column(BigInteger, nullable=False)
    role_id = Column(
        Integer,
        ForeignKey("user_roles.id"),
        nullable=False,
        default=UserRoleConstant.USER.value,
    )
    is_banned = Column(Boolean, default=False)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        return dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            town=self.town,
            telegram_id=self.telegram_id,
            role_id=self.role_id,
            is_banned=self.is_banned,
        )


class UserRole(BaseModel):
    """Модель пользовательских ролей."""

    __tablename__ = "user_roles"

    name = Column(String(150), nullable=False)
    users = relationship("User")


class Document(BaseModel):
    """Модель документов."""

    __tablename__ = "documents"

    name = Column(String(150), nullable=False)
    document_id = Column(String(300), unique=True, nullable=False)
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
    )

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            document_id=self.document_id,
            category_id=self.category_id,
        )


class Category(BaseModel):
    """Модель категорий документов."""

    __tablename__ = "categories"

    name = Column(String(150))
    document = relationship(
        "Document", cascade="all, delete", passive_deletes=True
    )

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
        )
