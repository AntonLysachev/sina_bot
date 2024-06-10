from .models import CastomersOrm, ReviewsOrm
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import select
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class ORM():

    def __init__(self, url=DATABASE_URL, echo=True, pool_size=5, max_overflow=5) -> None:
        self.url = url
        self.echo = echo
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        async_engine = create_async_engine(url=self.url,
                                           echo=self.echo,
                                           pool_size=self.pool_size,
                                           max_overflow=self.max_overflow)
        self.async_session_factory = async_sessionmaker(async_engine)

    async def execute_insert_query(self, query):
        async with self.async_session_factory() as session:
            session.add(query)
            await session.commit()

    async def execute_select_query(self, query, selection='scalars.all'):
        async with self.async_session_factory() as session:
            result = await session.execute(query)
            if selection == 'scalars.all':
                return result.scalars().all()
            if selection == 'all':
                return result.all()
            if selection == 'scalars.one':
                return result.scalars().one_or_none()

    async def add_customer(self, phone: str, chat_id: int, poster_id: int, group_name: str, firstname=None, lastname=None, birthday=None) -> None:
        customer = CastomersOrm(phone=phone, chat_id=chat_id, poster_id=poster_id, firstname=firstname, lastname=lastname, birthday=birthday, group_name=group_name)
        await self.execute_insert_query(customer)

    async def add_review(self, grade: int, customer_id: int, type: str, text=None) -> None:
        review = ReviewsOrm(review=text, grade=grade, customer_id=customer_id, type=type)
        await self.execute_insert_query(review)

    async def get_customer_by_chat_id(self, chat_id: int):
        query = select(CastomersOrm).where(CastomersOrm.chat_id == chat_id)
        return await self.execute_select_query(query, 'scalars.one')

    async def get_phone_by_chat_id(self, chat_id: int) -> str:
        query = select(CastomersOrm.phone).where(CastomersOrm.chat_id == chat_id)
        return await self.execute_select_query(query, 'scalars.one')

    async def get_full_name_by_chat_id(self, chat_id: int) -> str | None:
        query = select(CastomersOrm.firstname, CastomersOrm.lastname).where(CastomersOrm.chat_id == chat_id)
        full_name = await self.execute_select_query(query, 'all')
        full_name = full_name[0]
        if full_name is not None:
            return ' '.join(full_name)
        else:
            return None

    async def get_customer_id_by_chat_id(self, chat_id: int) -> int:
        query = select(CastomersOrm.id).where(CastomersOrm.chat_id == chat_id)
        return await self.execute_select_query(query, 'scalars.one')

    async def get_chat_id_by_poster_id(self, poster_id: int) -> int:
        query = select(CastomersOrm.chat_id).where(CastomersOrm.poster_id == poster_id)
        return self.execute_select_query(query, 'scalars.one')

    async def get_poster_id_by_chat_id(self, chat_id: int) -> int:
        query = select(CastomersOrm.poster_id).where(CastomersOrm.chat_id == chat_id)
        return await self.execute_select_query(query, 'scalars.one')

    async def get_admins(self):
        query = select(CastomersOrm.chat_id).where(CastomersOrm.group_name == 'admin')
        return await self.execute_select_query(query, 'scalars.all')

    async def select_customers(self):
        query = select(CastomersOrm)
        return await self.execute_select_query(query, 'scalars.all')

    async def update_customers_name(self, firstname: str, lastname: str, customer_id: int) -> None:
        async with self.async_session_factory() as session:
            customer = await session.get(CastomersOrm, customer_id)
            customer.firstname = firstname
            customer.lastname = lastname
            await session.commit()

    async def update_customer_phone(self, phone: int, customer_id: int) -> None:
        async with self.async_session_factory() as session:
            customer = await session.get(CastomersOrm, customer_id)
            customer.phone = phone
            await session.commit()
