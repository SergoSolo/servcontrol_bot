from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'
        
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)