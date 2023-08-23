"""Команды со слешем, которые Телеграм отрисовывает в меню бота"""
from aiogram import Bot
from aiogram.types import BotCommand


async def set_ui_commands(bot: Bot):
    """Установить команды"""
    commands = [
        BotCommand(command="start", description="Главное меню"),
    ]
    await bot.set_my_commands(commands=commands)
