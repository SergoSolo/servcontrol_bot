from datetime import datetime

from core.db.db import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


def fresh_timestamp() -> datetime:
    """Временная метка."""
    return datetime.utcnow


class BaseModel(Base):
    """Абстрактная модель с общими полями."""

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=fresh_timestamp())
    updated_at = Column(DateTime, onupdate=fresh_timestamp())
    deleted_at = Column(DateTime, onupdate=fresh_timestamp())


class User(BaseModel):

    __tablename__ = "users"

    name = Column(String(150))
    telegram_id = Column(Integer, nullable=False)
    is_staff = Column(Boolean, default=False)


class Document(BaseModel):

    __tablename__ = "documents"

    name = Column(String(150))
    doc_type_id = Column(Integer, ForeignKey("document_types.id"), nullable=False)


class DocumentType(BaseModel):

    __tablename__ = "document_types"

    name = Column(String(150))
    document = relationship("Document")
