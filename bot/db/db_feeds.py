import datetime

from sqlalchemy import desc, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.model_feed import Feed, FeedPost, UserFeed


async def get_user_feeds(session: AsyncSession, id_user: int) -> tuple[Feed] | None:
    db_query = await session.execute(
        select(Feed)
        .join(UserFeed, isouter=True)
        .where(UserFeed.id_user == id_user)
    )
    items_tuple = db_query.scalars().all()
    return items_tuple


async def get_feed(session: AsyncSession, id_feed: int) -> Feed | None:
    feed_item = await session.get(Feed, id_feed)
    return feed_item


async def delete_user_feed(session: AsyncSession, id_user: int, id_feed: int) -> bool:
    feed_user_item = await session.get(UserFeed, [id_user, id_feed])
    if feed_user_item:
        await session.delete(feed_user_item)
        await session.commit()

    return True


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

    db_query = await session.execute(
        select(FeedPost)
        .where(FeedPost.id_feed == feed_item.id)
        .order_by(desc(FeedPost.id))
    )
    feed_last_post_item = db_query.scalar()

    feed_user_item = await session.get(UserFeed, [id_user, feed_item.id])
    if not feed_user_item:
        feed_user_item = UserFeed(
            id_user=id_user,
            id_feed=feed_item.id,
            id_last_post=feed_last_post_item.id if feed_last_post_item else None
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


async def get_feeds_posts_for_send(session: AsyncSession):
    db_query = await session.execute(
        select(FeedPost, UserFeed, Feed)
        .join(UserFeed, FeedPost.id_feed == UserFeed.id_feed, isouter=True)
        .join(Feed, FeedPost.id_feed == Feed.id, isouter=True)
        .where(
            or_(
                UserFeed.id_last_post == None,
                UserFeed.id_last_post < FeedPost.id,
            )
        )
        .order_by(FeedPost.id)
        .limit(20)  # лимит Телеграма на кол-во сообщений от бота в одном чате за минуту
    )
    return db_query.all()


async def update_user_feeds_last_post(session: AsyncSession, results: list[tuple[int, int, int]]) -> bool:
    for id_user, id_feed, id_last_post in results:
        user_feed_item = await session.get(UserFeed, [id_user, id_feed])
        if user_feed_item:
            user_feed_item.id_last_post = id_last_post
            session.add(user_feed_item)

    await session.commit()
    return True
