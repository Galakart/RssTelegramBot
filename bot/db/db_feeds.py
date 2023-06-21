from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.model_feed import Feed, FeedPost, UserFeed


async def get_user_feeds(session: AsyncSession, id_user: int):
    db_query = await session.execute(
        select(Feed)
        .join(UserFeed, isouter=True)
        .where(UserFeed.id_user == id_user)
    )
    items_tuple = db_query.scalars().all()
    return items_tuple


async def add_feed(session: AsyncSession, link: str, title: str, id_user: int) -> bool:
    db_query = await session.execute(
        select(Feed)
        .where(Feed.link == link)
    )
    feed_item = db_query.scalar()
    if not feed_item:
        feed_item = Feed(
            link=link,
            title=title,
            id_author=id_user
        )
        session.add(feed_item)
        await session.flush()

    feed_user_item = await session.get(UserFeed, [id_user, feed_item.id])
    if not feed_user_item:
        feed_user_item = UserFeed(
            id_user=id_user,
            id_feed=feed_item.id
        )
        session.add(feed_user_item)

    await session.commit()
    return True
