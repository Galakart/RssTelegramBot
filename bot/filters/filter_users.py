"""Фильтры на статус пользователей"""
from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db import db_user


class IsUserReg(BaseFilter):
    """Пользователь зарегистрирован?"""
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        return await db_user.get_user(session, message.chat.id)
