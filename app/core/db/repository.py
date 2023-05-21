from sqlalchemy import select

from app.core.db.db import AsyncSessionLocal
from app.core.db.models import Category, Document, User


class CRUDBase:
    def __init__(self, model) -> None:
        self.model = model
        self.session = AsyncSessionLocal()

    async def get_object(self, object_id: int):
        async with self.session as session:
            db_object = await session.execute(
                select(self.model).where(self.model.id == object_id)
            )
            return db_object.scalars().first()

    async def get_all_objects(self):
        async with self.session as session:
            db_objects = await session.execute(select(self.model))
            return db_objects.scalars().all()

    async def create_object(self, data):
        async with self.session as session:
            object = self.model(**data)
            session.add(object)
            await session.commit()

    async def update_object(self, object_id: int, data: dict):
        async with self.session as session:
            db = await session.execute(
                select(self.model).where(self.model.id == object_id)
            )
            db_object = db.scalars().first()
            for field in db_object.to_dict():
                if field in data:
                    setattr(db_object, field, data[field])
            session.add(db_object)
            await session.commit()
            await session.refresh(db_object)

    async def delete_object(self, object_id: int):
        async with self.session as session:
            db = await session.execute(
                select(self.model).where(self.model.id == object_id)
            )
            db_object = db.scalars().first()
            await session.delete(db_object)
            await session.commit()


class UserCRUD(CRUDBase):
    async def get_users_telegram_ids_by_role(self, role_id: int):
        async with self.session as session:
            db_objects = await session.execute(
                select(self.model.telegram_id).where(
                    self.model.role_id == role_id
                )
            )
            return db_objects.scalars().all()

    async def get_users_by_filters(
        self, role_id: int, is_banned: bool = False
    ):
        async with self.session as session:
            db_objects = await session.execute(
                select(self.model).where(
                    self.model.role_id == role_id,
                    self.model.is_banned == is_banned,
                )
            )
            return db_objects.scalars().all()

    async def get_user_by_telegram_id(self, telegram_id: int):
        async with self.session as session:
            db_object = await session.execute(
                select(self.model).where(self.model.telegram_id == telegram_id)
            )
            return db_object.scalars().first()


class DocumentCRUD(CRUDBase):
    async def get_all_documents_by_type(self, type_id):
        async with self.session as session:
            db_objects = await session.execute(
                select(self.model).where(self.model.category_id == type_id)
            )
            return db_objects.scalars().all()

    async def get_documents_id_by_type(self, type_id: int):
        async with self.session as session:
            db_objects = await session.execute(
                select(self.model.document_id).where(
                    self.model.category_id == type_id
                )
            )
            return db_objects.scalars().all()


class CategoryCRUD(CRUDBase):
    pass


user_service = UserCRUD(User)
document_service = DocumentCRUD(Document)
category_service = CategoryCRUD(Category)
