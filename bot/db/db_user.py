"""Операции в БД с пользователями"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.model_user import User


async def get_user(session: AsyncSession, id_user: int) -> User | None:
    """Выбрать пользователя по id"""
    db_query = await session.execute(
        select(User)
        .where(User.id == id_user)
    )
    item = db_query.scalar()
    return item


async def get_all_active_users(session: AsyncSession):
    """Все активные пользователи"""
    db_query = await session.execute(
        select(User)
        .where(User.active == True)
    )
    items_tuple = db_query.scalars().all()
    return items_tuple


async def add_user(session: AsyncSession, id_user: int, nick: str | None) -> bool:
    """Добавить пользователя"""
    new_user = User(
        id=id_user,
        nick=nick,
        active=1
    )
    session.add(new_user)
    await session.commit()
    return True

# async def del_user(session: AsyncSession, id_user: int) -> bool:
#     """Удалить пользователя"""
#     item = await session.get(User, id_user)
#     if item:
#         await session.delete(item)
#         await session.commit()
#         return True
#     return False
