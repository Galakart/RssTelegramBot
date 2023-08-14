from enum import Enum, unique
from typing import Optional

from aiogram.filters.callback_data import CallbackData


@unique
class FeedActions(Enum):
    DELETE = 1


class FeedsListFactory(CallbackData, prefix="feeds_list"):
    id_feed: int
    # opt_var: Optional[int]


class FeedActionsFactory(CallbackData, prefix="feed_actions"):
    id_feed: int
    action: int
