from sqlalchemy import insert, select, delete, update
from app.database import async_session_maker



class BaseDAO:
    """Class for working with DB"""

    model = None


    # Метод поиска в БД по id
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(id=model_id)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        

    # Метод поиска в БД что-то одного или ничего
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()
        

    # Метод поиска всех значений по фильтру
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
        

    # Метод добавления в БД
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
