from sqlalchemy import insert, select, delete, update
from app.database import async_session_maker



class BaseDAO:
    """Class for working with DB"""

    model = None


    # Find by id
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        

    # Find something one or None
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        

    # Find all dates
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
        

    # Method for adding new string to DB
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            await session.execute(stmt)
            await session.commit()


    # Метод для обновления данных
    @classmethod
    async def update(cls, model_id: int, data: dict):
        async with async_session_maker() as session:
            stmt = update(cls.model).where(cls.model.id == model_id).values(**data)
            await session.execute(stmt)
            await session.commit()


    # Delete dates
    @classmethod
    async def delete(cls, **filter):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter)
            await session.execute(query)
            await session.commit()
