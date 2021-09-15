import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src.tgbot.config import load_config
from src.tgbot.filters.role import RoleFilter, AdminFilter
from src.tgbot.handlers.admin import register_admin
from src.tgbot.handlers.user import register_user
from src.tgbot.middlewares.db import DbMiddleware
from src.tgbot.middlewares.role import RoleMiddleware
from src.tgbot.middlewares.dialog import DialogMiddleware
from src.db.database import session_scope

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config()

    if config.tg_bot.use_redis:
        storage = MemoryStorage()  # AIORedis raises error
    else:
        storage = MemoryStorage()

    with session_scope() as session:
        bot = Bot(token=config.tg_bot.token)
        dp = Dispatcher(bot, storage=storage)
        dp.middleware.setup(DbMiddleware(session))
        dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_ids))
        dp.middleware.setup(DialogMiddleware())
        dp.filters_factory.bind(RoleFilter)
        dp.filters_factory.bind(AdminFilter)

        register_admin(dp)
        register_user(dp)

        # start
        try:
            await dp.start_polling()
        finally:
            await dp.storage.close()
            await dp.storage.wait_closed()
            await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
