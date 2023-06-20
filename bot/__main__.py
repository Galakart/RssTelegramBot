"""Main bot"""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from pygelf import GelfUdpHandler
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot.config_reader import config
from bot.handlers import router_commands
from bot.middlewares import DbSessionMiddleware
from bot.ui_commands import set_ui_commands

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


async def main():
    engine = create_async_engine(url=config.db_url, echo=False)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    dp = Dispatcher(storage=RedisStorage(redis=RedisStorage.from_url("redis://redis:6379/0").redis))
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    dp.include_router(router_commands.router)

    await set_ui_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
