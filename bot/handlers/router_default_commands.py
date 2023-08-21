"""Стандартные команды для бота, работающие в первую очередь"""
from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.filter_users import IsUserReg

from .shared_actions import reg_user, show_mainmenu

router = Router(name="router_default_commands")


@router.message(IsUserReg(), Command("start"))
async def cmd_start_registered(message: Message, state: FSMContext):
    """Команда /start от зарегистрированного пользователя"""
    await show_mainmenu(message, state)


@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession, state: FSMContext):
    """Команда /start от незарегистрированного пользователя"""
    if await reg_user(message, session):
        await show_mainmenu(message, state)


@router.message(IsUserReg(), Text('Отмена'))
async def cmd_cancel(message: Message, state: FSMContext):
    """Возврат в главное меню из любого места по тексту Отмена"""
    await show_mainmenu(message, state)
