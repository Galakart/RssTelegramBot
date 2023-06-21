from sqlalchemy import BigInteger, Boolean, Column, Text

from .base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"comment": "Юзеры"}

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    nick = Column(Text)
    active = Column(Boolean, nullable=False, default=True)
