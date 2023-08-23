"""Общие методы для нескольких роутеров"""
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot import keyboards
from bot.db import db_user


async def reg_user(message: Message, session: AsyncSession) -> bool:
    """Регистрация пользователя"""
    user_item = await db_user.get_user(session, message.chat.id)
    if user_item:
        return True

    if not message.from_user:
        return False

    all_users_tuple = await db_user.get_all_active_users(session)
    if not all_users_tuple:
        await db_user.add_user(session, message.chat.id, message.from_user.username)
        await message.answer('Вы зарегистрированы как первый пользователь в боте')
        return True

    # FIXME регистрация допускает только одного пользователя, но технический сам бот может работать с несколькими.
    # Мне сейчас функционал с несколькими не нужен.
    mes = (
        'В боте уже зареган один пользователь\n'
        'Регистрация доступна только для одного пользователя'
    )
    await message.answer(mes, reply_markup=keyboards.remove_keyb())
    return False


async def show_mainmenu(message: Message, state: FSMContext):
    """Перейти в главное меню"""
    await state.clear()
    await message.answer('Вы в главном меню', reply_markup=keyboards.get_mainmenu_keyb())
