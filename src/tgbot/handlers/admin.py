from aiogram import Dispatcher
from aiogram.types import Message

from src.tgbot.models.role import UserRole


async def admin_start(m: Message):
    await m.reply("Hello, admin!")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, commands=["start"], state="*", role=UserRole.ADMIN
    )
    # # or you can pass multiple roles:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", role=[UserRole.ADMIN])
    # # or use another filter:
    # dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
