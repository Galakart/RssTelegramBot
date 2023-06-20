from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.filter_users import IsUserReg

from .actions import reg_user, show_mainmenu

router = Router(name="router_default_commands")


@router.message(IsUserReg(), Command("start"))
async def cmd_start_registered(message: Message):
    await show_mainmenu(message)


@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession):
    if await reg_user(message, session):
        await show_mainmenu(message)
