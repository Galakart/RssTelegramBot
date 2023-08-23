"""Состояния в боте"""
from aiogram.fsm.state import State, StatesGroup

# pylint: disable=too-few-public-methods


class NewFeedState(StatesGroup):
    """Запрос ссылки на новую ленту"""
    ask_newfeed_link = State()
