from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot import keyboards
from bot.db import db_user


async def reg_user(message: Message, session: AsyncSession) -> bool:
    user_item = await db_user.get_user(session, message.chat.id)
    if user_item:
        return True

    all_users_tuple = await db_user.get_all_active_users(session)
    if not all_users_tuple:
        await db_user.add_user(session, message.chat.id, message.from_user.username)
        await message.answer('Вы зарегистрированы как первый пользователь в боте')
        return True

    mes = (
        'В боте уже зареган один пользователь\n'
        'Регистрация доступна только для одного пользователя'
    )
    await message.answer(mes, reply_markup=keyboards.remove_keyb())
    return False


async def show_mainmenu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы в главном меню', reply_markup=keyboards.get_mainmenu_keyb())
