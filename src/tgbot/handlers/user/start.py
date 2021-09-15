from aiogram.types import Message

from src.tgbot.services.repository import TelegramUserRepo


async def user_start(
    msg: Message,
    tg_user_repo: TelegramUserRepo,
):
    user = tg_user_repo.get_or_create(
        telegram_id=msg.from_user.id,
        first_name=msg.from_user.first_name,
        last_name=msg.from_user.last_name,
        default="telegram_id",
    )
    await msg.reply("Hello, {}!".format(user.full_name))
