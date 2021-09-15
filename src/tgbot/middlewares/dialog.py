from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from src.core.tgbot import dialog


class DialogMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        data["dialog"] = dialog

    async def post_process(self, obj, data, *args):
        del data["dialog"]
