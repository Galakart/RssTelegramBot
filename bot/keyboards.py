"""Сборка клавиатур бота"""
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup, ReplyKeyboardRemove)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.cbdata import FeedActions, FeedActionsFactory, FeedsListFactory
from bot.models.model_feed import Feed


def remove_keyb() -> ReplyKeyboardRemove:
    """Просто пустая клавиатура"""
    return ReplyKeyboardRemove(remove_keyboard=True)


def get_mainmenu_keyb() -> ReplyKeyboardMarkup:
    """Клавиатура главного меню"""
    keyb = ReplyKeyboardBuilder()
    keyb.button(text="Мои ленты")
    keyb.button(text="Подписаться на новую")
    keyb.adjust(2)
    return keyb.as_markup(resize_keyboard=True)


def get_onlycancel_keyb() -> ReplyKeyboardMarkup:
    """Клавиатура только с кнопкой Отмена"""
    keyb = ReplyKeyboardBuilder()
    keyb.button(text="Отмена")
    return keyb.as_markup(resize_keyboard=True)


def get_cancel_accept_keyb() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопками Отмена и Далее"""
    keyb = ReplyKeyboardBuilder()
    keyb.button(text="Отмена")
    keyb.button(text="Далее")
    keyb.adjust(2)
    return keyb.as_markup(resize_keyboard=True)


def get_feeds_list_inlinekeyb(feeds_tuple: tuple[Feed]) -> InlineKeyboardMarkup:
    """Инлайн-клавиатура со списком лент"""
    keyb = InlineKeyboardBuilder()

    # FIXME сделать пагинацию, если много подписок
    for feed_item in feeds_tuple:
        keyb.add(InlineKeyboardButton(
            text=feed_item.title,  # type: ignore
            callback_data=FeedsListFactory(id_feed=feed_item.id).pack())  # type: ignore
        )

    keyb.adjust(1)
    return keyb.as_markup()


def get_feed_actions_inlinekeyb(id_feed: int) -> InlineKeyboardMarkup:
    """Клавиатура со списком действий над конкретной лентой"""
    keyb = InlineKeyboardBuilder()

    keyb.add(InlineKeyboardButton(
        text='❌Удалить',
        callback_data=FeedActionsFactory(id_feed=id_feed, action=FeedActions.DELETE.value).pack())
    )

    keyb.adjust(1)
    return keyb.as_markup()
