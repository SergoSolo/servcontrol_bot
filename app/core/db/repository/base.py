from core.config import settings
from core.db.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_async_engine(settings.database_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


class CRUDBase:
    def __init__(self, model) -> None:
        self.model = model
        self.session = AsyncSessionLocal()

    async def get_multi(self, session: AsyncSession):
        async with self.session as session:
            db_objects = await session.execute(select(self.model))
            return db_objects.scalars.all()

    async def get(self, object_id: int, session: AsyncSession):
        async with self.session as session:
            db_object = await session.execute(
                select(self.model).where(self.model.id == object_id)
            )
            return db_object


class UserCRUD(CRUDBase):
    async def is_staff(self, telegram_id: int):
        async with self.session as session:
            db_object = await session.execute(
                select(self.model.is_staff).where(self.model.telegram_id == telegram_id)
            )
            return db_object.scalars().first()


user_service = UserCRUD(User)
