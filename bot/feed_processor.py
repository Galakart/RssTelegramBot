"""Операции по таймеру с RSS-лентами"""
import datetime
import logging
import re
import time

import feedparser
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from bot.db import db_feeds
from bot.models.model_feed import Feed, FeedPost, UserFeed

LOGGER = logging.getLogger()

# html-теги, которые разрешено отправлять в телеграме при parse_mode="HTML"
TG_ALLOWED_TAGS = [
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

# ограничение телеграма на количество сообщений в одном чате в минуту
TG_MAX_MESSAGES_COUNT_PER_MINUTE = 20


async def update_feeds(async_session: async_sessionmaker[AsyncSession]):
    """Обновление лент (поиск и сохранение новых постов)"""
    async with async_session() as session:
        feeds_tuple = await db_feeds.get_feeds_for_update(session)  # FIXME сейчас период обновления для всех 12 часов
        feed_posts_lst = []

        feed_item: Feed
        for feed_item in feeds_tuple:
            last_post = await db_feeds.get_feed_last_post(session, feed_item.id)  # type: ignore
            LOGGER.info('feedparser is parsing the feed %s', feed_item.title)
            rss_data = feedparser.parse(feed_item.link)
            if 'title' not in rss_data.feed:
                LOGGER.warning('Не удалось скачать данные ленты %s: %s', feed_item.id, feed_item.title)
                continue

            # Если ленту недавно добавили (нет загруженных постов), то сохраним только 5 самых новых,
            # чтобы не захламлять отправку старыми постами.
            count_posts_for_search = None if last_post else 5

            for entry in reversed(rss_data.entries[:count_posts_for_search]):
                datetime_published = datetime.datetime.fromtimestamp(time.mktime(entry.published_parsed))
                if last_post and last_post.datetime_published >= datetime_published:  # type: ignore
                    continue

                # регулярка удаляет все html-теги в строке,
                # кроме тех что в TG_ALLOWED_TAGS
                # также удаляет всякое в стиле &nbsp;
                # за регулярку спасибо ChatGPT
                description_clean = entry.description.replace('<br />', '\n')
                description_clean = re.compile(rf'<(?!\/?(?:{"|".join(TG_ALLOWED_TAGS)})(?=>|\s.*>))\/?.*?>|(&.*?;)') \
                    .sub('', description_clean)

                new_feed_post = FeedPost(
                    id_feed=feed_item.id,
                    title=entry.title,
                    description=description_clean,
                    link=entry.link,
                    datetime_published=datetime_published
                )
                feed_posts_lst.append(new_feed_post)

            feed_item.datetime_last_update = datetime.datetime.now()  # type: ignore
            await db_feeds.update_feed(session, feed_item)

        if feed_posts_lst:
            await db_feeds.add_feed_posts_lst(session, feed_posts_lst)


async def send_feeds(async_session: async_sessionmaker[AsyncSession], bot: Bot):
    """Отправка постов пользователям"""
    async with async_session() as session:
        feeds_posts_tuple = await db_feeds.get_feeds_posts_for_send(session)
        if not feeds_posts_tuple:
            return

        results_lst = []
        sent_count = 0

        feed_post_item: FeedPost
        user_feed_item: UserFeed
        feed_item: Feed
        for row_item in feeds_posts_tuple:
            feed_post_item, user_feed_item, feed_item = row_item

            mes = (
                f'<b>{feed_item.title}</b>\n\n'
                f'<i>{feed_post_item.title}</i>\n'
                f'{feed_post_item.description}\n\n'
                f'Ссылка: {feed_post_item.link}'
            )

            try:
                if len(mes) > 4095:
                    for offset in range(0, len(mes), 4095):
                        await bot.send_message(user_feed_item.id_user, mes[offset:offset + 4095])  # type: ignore
                        sent_count += 1
                else:
                    await bot.send_message(user_feed_item.id_user, mes)  # type: ignore
                    sent_count += 1
            except Exception as ex:
                LOGGER.error(ex)
                continue

            results_lst.append((user_feed_item.id_user, feed_post_item.id_feed, feed_post_item.id))

            if sent_count >= TG_MAX_MESSAGES_COUNT_PER_MINUTE:
                break

        await db_feeds.update_user_feeds_last_post(session, results_lst)
