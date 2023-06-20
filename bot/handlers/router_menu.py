from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.filter_users import IsUserReg

router = Router(name="router_menu")
router.message.filter(IsUserReg())


@router.message(Text('Мои ленты'))
async def cmd_myfeeds(message: Message, session: AsyncSession):
    await message.answer('Список лент недоступен')
