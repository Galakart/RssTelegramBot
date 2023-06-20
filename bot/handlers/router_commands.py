from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot import keyboards
from bot.db import db_user

router = Router(name="router_commands")


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, session: AsyncSession):
    if check_user_reg(message, session):
        await mainmenu(message)


async def check_user_reg(message: Message, session: AsyncSession) -> bool:
    user_item = await db_user.get_user(session, message.chat.id)
    if user_item:
        await message.answer('Ok')
        return True

    all_users_tuple = await db_user.get_all_active_users(session)
    if not all_users_tuple:
        await db_user.add_user(session, message.chat.id, message.from_user.username)
        await message.answer('Вы зареганы как первый юзер в боте')
        return True

    mes = (
        'В боте уже зареган один юзер\n'
        'Регистрация доступна только для одного юзера'
    )
    await message.answer(mes, reply_markup=keyboards.remove_keyb())
    return False


async def mainmenu(message: Message):
    await message.answer('Вы в главном меню', reply_markup=keyboards.get_mainmenu_keyb())
