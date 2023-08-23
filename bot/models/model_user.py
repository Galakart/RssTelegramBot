"""Модели пользователей"""
from sqlalchemy import BigInteger, Boolean, Column, Text

from .base import Base

# pylint: disable=too-few-public-methods


class User(Base):
    """Юзеры бота"""
    __tablename__ = "users"
    __table_args__ = {"comment": "Юзеры"}

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    nick = Column(Text)
    active = Column(Boolean, nullable=False, default=True)
