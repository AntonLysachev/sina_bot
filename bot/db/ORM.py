from .models import CastomersOrm, ReviewsOrm
from .database import async_engine, async_session_factory
from sqlalchemy import select


async def create_customers_table() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(CastomersOrm.metadata.create_all)


async def create_reviews_table() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(ReviewsOrm.metadata.create_all)


async def add_customer(phone: str, chat_id: int, poster_id: int, group_name: str, firstname=None, lastname=None, birthday=None) -> None:
    customer = CastomersOrm(phone=phone, chat_id=chat_id, poster_id=poster_id, firstname=firstname, lastname=lastname, birthday=birthday, group_name=group_name)
    async with async_session_factory() as session:
        session.add(customer)
        await session.commit()


async def add_review(grade: int, customer_id: int, type: str, text=None) -> None:
    review = ReviewsOrm(review=text, grade=grade, customer_id=customer_id, type=type)
    async with async_session_factory() as sesion:
        sesion.add(review)
        await sesion.commit()


async def get_customer_by_chat_id(chat_id: int):
    async with async_session_factory() as session:
        query = select(CastomersOrm).where(CastomersOrm.chat_id == chat_id)
        result = await session.execute(query)
        customer = result.scalars().one_or_none()
        return customer


async def get_phone_by_chat_id(chat_id: int) -> str:
    async with async_session_factory() as session:
        query = select(CastomersOrm.phone).where(CastomersOrm.chat_id == chat_id)
        result = await session.execute(query)
        phone = result.scalars().one_or_none()
        return phone


async def get_full_name_by_chat_id(chat_id: int) -> str | None:
    async with async_session_factory() as session:
        query = select(CastomersOrm.firstname, CastomersOrm.lastname).where(CastomersOrm.chat_id == chat_id)
        result = await session.execute(query)
        full_name = result.all()[0]
        if full_name is not None:
            return ' '.join(full_name)
        else:
            return None


async def get_customer_id_by_chat_id(chat_id: int) -> int:
    async with async_session_factory() as session:
        query = select(CastomersOrm.id).where(CastomersOrm.chat_id == chat_id)
        result = await session.execute(query)
        customer = result.scalars().one_or_none()
        return customer


async def get_chat_id_by_poster_id(poster_id: int) -> int:
    async with async_session_factory() as session:
        query = select(CastomersOrm.chat_id).where(CastomersOrm.poster_id == poster_id)
        result = await session.execute(query)
        chat_id = result.scalars().one_or_none()
        print(chat_id)
        return chat_id


async def get_poster_id_by_chat_id(chat_id: int) -> int:
    async with async_session_factory() as session:
        query = select(CastomersOrm.poster_id).where(CastomersOrm.chat_id == chat_id)
        result = await session.execute(query)
        poster_id = result.scalars().one_or_none()
        return poster_id


async def get_admins():
    async with async_session_factory() as session:
        query = select(CastomersOrm.chat_id).where(CastomersOrm.group_name == 'admin')
        result = await session.execute(query)
        admins = result.scalars().all()
        return admins


async def select_customers():
    async with async_session_factory() as session:
        query = select(CastomersOrm)
        result = await session.execute(query)
        customers = result.scalars().all()
        return customers


async def update_customers_name(firstname, lastname, customer_id) -> None:
    async with async_session_factory() as session:
        customer = await session.get(CastomersOrm, customer_id)
        customer.firstname = firstname
        customer.lastname = lastname
        await session.commit()


async def update_customer_phone(phone: int, customer_id: int) -> None:
    async with async_session_factory() as session:
        customer = await session.get(CastomersOrm, customer_id)
        customer.phone = phone
        await session.commit()
