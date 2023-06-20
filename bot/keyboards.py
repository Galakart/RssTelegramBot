from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def remove_keyb() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove(remove_keyboard=True)


def get_mainmenu_keyb() -> ReplyKeyboardMarkup:
    keyb = ReplyKeyboardBuilder()
    keyb.button(text="Мои ленты")
    keyb.button(text="Подписаться на новую")
    keyb.adjust(2)
    return keyb.as_markup(resize_keyboard=True)
