import datetime
import logging
import re
import time

import feedparser
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.db import db_feeds
from bot.models.model_feed import Feed, FeedPost

LOGGER = logging.getLogger()

allowed_tags = [
    'b',
    'strong',
    'i',
    'em',
    'u',
    'ins',
    's',
    'strike',
    'del',
    'a',
    'code',
    'pre',
]


async def update_feeds(async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        feeds_tuple = await db_feeds.get_feeds_for_update(session)  # TODO сейчас период обновления для всех 12 часов
        feed_posts_lst = []

        feed_item: Feed
        for feed_item in feeds_tuple:
            last_post = await db_feeds.get_feed_last_post(session, feed_item.id)
            d = feedparser.parse(feed_item.link)
            if 'title' not in d.feed:
                LOGGER.warning('Не удалось скачать данные ленты %s: %s', feed_item.id, feed_item.title)
                continue

            # Если ленту недавно добавили (нет загруженных постов), то сохраним только 5 самых новых,
            # чтобы не захламлять отправку старыми постами.
            count_posts_for_search = None if last_post else 5

            for entry in reversed(d.entries[:count_posts_for_search]):
                datetime_published = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
                if last_post and last_post.datetime_published >= datetime_published:
                    continue

                # регулярка удаляет все html-теги в строке,
                # кроме тех что в allowed_tags (разрешённые в telegram parse_mode='html')
                # также удаляет всякое в стиле &nbsp;
                # за регулярку спасибо ChatGPT
                description_clean = re.compile(rf'<(?!\/?(?:{"|".join(allowed_tags)})(?=>|\s.*>))\/?.*?>|(&.*?;)').sub('', entry.description)

                new_feed_post = FeedPost(
                    id_feed=feed_item.id,
                    title=entry.title,
                    description=description_clean,
                    link=entry.link,
                    datetime_published=datetime_published
                )
                feed_posts_lst.append(new_feed_post)

            feed_item.datetime_last_update = datetime.datetime.now()
            await db_feeds.update_feed(session, feed_item)

        if feed_posts_lst:
            await db_feeds.add_feed_posts_lst(session, feed_posts_lst)


# if len(description_clean) > 4095:
#     for x in range(0, len(description_clean), 4095):
#         await message.answer(description_clean[x:x+4095])
# else:
#     await message.answer(description_clean)
