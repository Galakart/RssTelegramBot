import datetime

from sqlalchemy import desc, or_, select
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


async def get_feeds_for_update(session: AsyncSession):
    db_query = await session.execute(
        select(Feed)
        .where(
            or_(
                Feed.datetime_last_update == None,
                Feed.datetime_last_update <= datetime.datetime.now() - datetime.timedelta(hours=12),
            )
        )
    )
    items_tuple = db_query.scalars().all()
    return items_tuple


async def get_feed_last_post(session: AsyncSession, id_feed: int) -> FeedPost | None:
    db_query = await session.execute(
        select(FeedPost)
        .where(FeedPost.id_feed == id_feed)
        .order_by(desc(FeedPost.id))
    )
    item = db_query.scalar()
    return item


async def add_feed_posts_lst(session: AsyncSession, feed_posts_lst: list[FeedPost]) -> bool:
    session.add_all(feed_posts_lst)
    await session.commit()
    return True


async def update_feed(session: AsyncSession, new_feed_item: Feed) -> bool:
    feed_item = await session.get(Feed, new_feed_item.id)
    if feed_item:
        feed_item.datetime_last_update = new_feed_item.datetime_last_update  # TODO пока только это поле
        session.add(feed_item)
        await session.commit()

    return True
