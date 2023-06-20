from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.model_user import User


async def get_user(session: AsyncSession, id_user: int) -> User | None:
    db_query = await session.execute(
        select(User)
        .where(User.id == id_user)
    )
    item = db_query.scalar()
    print(item)
    return item


async def get_all_active_users(session: AsyncSession):
    db_query = await session.execute(
        select(User)
        .where(User.active == True)
    )
    items_tuple = db_query.scalars().all()
    print(items_tuple)
    return items_tuple


async def add_user(session: AsyncSession, id_user: int, nick: str | None) -> bool:
    new_user = User(
        id=id_user,
        nick=nick,
        active=1
    )
    session.add(new_user)
    await session.commit()
    return True
