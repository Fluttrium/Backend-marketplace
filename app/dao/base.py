
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete, insert, select, update
from app.utils.manage import manage_session
from app.logger import logger

from app.database import async_session_maker


class BaseDAO:
        model = None

        @classmethod
        async def find_by_id(
                cls,
                **data,
        ) -> model:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**data).returning(cls.model)


                result = await session.execute(query)

                return result.scalar_one_or_none()

        @classmethod
        async def find_one_or_none(cls, **filter_by) -> model:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)

                result = await session.execute(query)

                return result.scalar_one_or_none()

        @classmethod
        async def find_all(cls):
            async with async_session_maker() as session:
                query = select(cls.model).order_by(cls.model.name)

                result = await session.execute(query)

                values = result.scalars().all()

                return values

        @classmethod
        async def validate_by_id(cls, value):
            async with async_session_maker() as session:
                query = select(cls.model).where(cls.model.id == value)

                result = (await session.execute(query)).scalar_one_or_none()

                return result

        @classmethod
        async def add(cls, **data):
            """Добавление нового объекта и возврат созданного объекта"""
            try:
                async with async_session_maker() as session:
                    query = insert(cls.model).values(**data).returning(cls.model)
                    result = await session.execute(query)
                    await session.commit()
                    return result.scalar_one()
            except SQLAlchemyError as e:
                logger.error(f"Error adding to {cls.model.__name__}: {e}")
                raise

        @classmethod
        @manage_session
        async def _create(cls, session=None, **data):
            create_query = insert(cls.model).values(**data).returning(cls.model)

            result = await session.execute(create_query)
            await session.commit()

            return result.scalar_one()

        @classmethod
        @manage_session
        async def update_data(cls, model_id, data, session=None):
            update_item_query = (
                update(cls.model)
                .where(cls.model.id == model_id)
                .values(**data)
                .returning(cls.model)
            )

            updated_item = await session.execute(update_item_query)
            await session.commit()

            return updated_item.scalars().one()

        @classmethod
        @manage_session
        async def delete_certain_item(cls, model_id, session=None):
            delete_item_query = delete(cls.model).where(cls.model.id == model_id)

            await session.execute(delete_item_query)
            await session.commit()

            return None