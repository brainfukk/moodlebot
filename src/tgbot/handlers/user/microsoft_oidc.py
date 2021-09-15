from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from src.core.tgbot import dialog as DialogModule
from src.tgbot.models.states import MicrosoftOIDCCredentialsState
from src.tgbot.services.repository import (
    MicrosoftOIDCCredentialsRepo,
    TelegramUserRepo,
)
from src.tgbot.tasks import auth_user

from .utils import validate_email


async def start_microsoft_oidc_dialog(msg: Message, dialog: DialogModule):
    await MicrosoftOIDCCredentialsState.email.set()
    await msg.reply(dialog.REQUEST_MCS_OIDC_EMAIL)


async def handle_email_microsoft_oidc_dialog(
    msg: Message, dialog: DialogModule, state: FSMContext
):
    if not validate_email(msg.text.strip()):
        await msg.reply(dialog.REQUEST_MCS_OIDC_EMAIL_NOT_CORRECT_FORMAT)
        return await start_microsoft_oidc_dialog(msg, dialog)

    async with state.proxy() as data:
        data["email"] = msg.text

    await msg.reply(dialog.REQUEST_MCS_OIDC_PWD)
    await MicrosoftOIDCCredentialsState.password.set()


async def handle_pwd_microsoft_oidc_dialog(
    msg: Message,
    dialog: DialogModule,
    state: FSMContext,
    tg_user_repo: TelegramUserRepo,
    mcs_oidc_repo: MicrosoftOIDCCredentialsRepo,
):
    async with state.proxy() as data:
        email = data["email"]
        pwd = msg.text.strip()

    user = tg_user_repo.get(telegram_id=msg.from_user.id)
    mcs_oidc_repo.update_or_create(
        telegram_user_id=user.id, email=email, password=pwd, default="telegram_user_id"
    )
    await msg.reply(dialog.REQUEST_MCS_STATUS_SUCCESS)
    auth_user.delay(user_id=user.id)
    await msg.bot.send_message(chat_id=msg.chat.id, text=dialog.AUTH_TASK_REGISTERED)
