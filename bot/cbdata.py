"""Данные в коллбэках"""
from enum import Enum, unique

from aiogram.filters.callback_data import CallbackData


@unique
class FeedActions(Enum):
    """Enum действий с лентой"""
    DELETE = 1


class FeedsListFactory(CallbackData, prefix="feeds_list"):
    """Для кнопок с названиями лент"""
    id_feed: int


class FeedActionsFactory(CallbackData, prefix="feed_actions"):
    """Для кнопок действий с конкретной лентой"""
    id_feed: int
    action: int
