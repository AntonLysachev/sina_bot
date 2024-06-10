from sqlalchemy import Integer, String, BigInteger, MetaData, Text, ForeignKey, text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from datetime import date, datetime


class Base(DeclarativeBase):
    pass


class CastomersOrm(Base):

    __tablename__ = 'customers'

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(unique=True, nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger(), unique=True, nullable=False)
    poster_id: Mapped[int] = mapped_column(BigInteger(), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=True)
    lastname: Mapped[str] = mapped_column(String(50), nullable=True)
    birthday: Mapped[date] = mapped_column(nullable=True)
    group_name: Mapped[str] = mapped_column(String(10), nullable=False)
    is_active: Mapped[bool] = mapped_column(server_default=text("true"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)


metadata_obj = MetaData()


class ReviewsOrm(Base):

    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)
    review: Mapped[str] = mapped_column(Text, nullable=True)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey('customers.id', ondelete='CASCADE'))
    type: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
