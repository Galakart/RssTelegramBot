"""Main bot"""
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.storage.redis import RedisStorage
from pygelf import GelfUdpHandler

from bot.config_reader import config

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
gelf_handler = GelfUdpHandler(
    host=config.graylog_host,
    port=12201,
    debug=True,
    _appname=config.compose_project_name,
)
LOGGER.addHandler(gelf_handler)


bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=RedisStorage(redis=RedisStorage.from_url("redis://redis:6379").redis))


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
