import feedparser
from aiogram import Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot import keyboards
from bot.cbdata import FeedActions, FeedActionsFactory, FeedsListFactory
from bot.db import db_feeds
from bot.filters.filter_users import IsUserReg
from bot.states import NewFeedState

from .shared_actions import show_mainmenu

router = Router(name="router_menu")
router.message.filter(IsUserReg())


@router.message(Text('Мои ленты'))
async def cmd_myfeeds(message: Message, session: AsyncSession):
    feeds_tuple = await db_feeds.get_user_feeds(session, message.chat.id)
    if not feeds_tuple:
        await message.answer('Вы не подписаны ни на одну ленту')
        return

    await message.answer("Подписки:", reply_markup=keyboards.get_feeds_list_inlinekeyb(feeds_tuple))


@router.callback_query(FeedsListFactory.filter())
async def cmd_feed_info(callback: CallbackQuery, callback_data: FeedsListFactory, session: AsyncSession):
    feed_item = await db_feeds.get_feed(session, callback_data.id_feed)
    mes = (
        f'{feed_item.title}\n'
        f'Ссылка: {feed_item.link}'
    )

    await callback.message.answer(mes, reply_markup=keyboards.get_feed_actions_inlinekeyb(feed_item.id))
    await callback.answer()


@router.callback_query(FeedActionsFactory.filter())
async def cmd_feed_action(callback: CallbackQuery, callback_data: FeedActionsFactory, session: AsyncSession):
    if callback_data.action == FeedActions.DELETE.value:
        result = await db_feeds.delete_user_feed(session, callback.from_user.id, callback_data.id_feed)
        mes = 'Лента удалена' if result else 'Ошибка удаления ленты'
        await callback.message.answer(mes)

    await callback.answer()


@router.message(Text('Подписаться на новую'))
async def cmd_newfeed_link_ask(message: Message, state: FSMContext):
    await message.answer('Введите ссылку на RSS-ленту', reply_markup=keyboards.get_onlycancel_keyb())
    await state.set_state(NewFeedState.ask_newfeed_link)


@router.message(NewFeedState.ask_newfeed_link)
async def cmd_newfeed_link_save(message: Message, state: FSMContext):
    link = message.text
    d = feedparser.parse(link)
    if 'title' not in d.feed:
        await message.answer('Ссылка не распознана как RSS-лента')
        await show_mainmenu(message, state)
        return
    title = d.feed.title

    await state.update_data(link=link, title=title)
    mes = (
        'Название RSS-ленты будет:\n'
        f'<b>{title}</b>\n\n'
        'Нажмите кнопку Далее, или введите прямо тут своё название'
    )
    await message.answer(mes, reply_markup=keyboards.get_cancel_accept_keyb())
    await state.set_state(NewFeedState.ask_newfeed_customtitle)


@router.message(NewFeedState.ask_newfeed_customtitle)
async def cmd_newfeed_customtitle_save(message: Message, session: AsyncSession, state: FSMContext):
    if message.text != 'Далее':
        await state.update_data(title=message.text)

    user_data = await state.get_data()
    if await db_feeds.add_feed(session, user_data['link'], user_data['title'], message.chat.id):
        await message.answer('RSS-лента добавлена')
    else:
        await message.answer('Ошибка при сохранении')

    await show_mainmenu(message, state)
