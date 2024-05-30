import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

async_engine = create_async_engine(
    url=DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=5)


async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
