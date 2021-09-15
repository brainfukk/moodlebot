from aiogram import Dispatcher

from src.tgbot.models.states import MicrosoftOIDCCredentialsState

from .microsoft_oidc import (
    handle_email_microsoft_oidc_dialog,
    handle_pwd_microsoft_oidc_dialog,
    start_microsoft_oidc_dialog,
)
from .start import user_start


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        user_start,
        commands=["start"],
        state="*",
    )
    dp.register_message_handler(
        start_microsoft_oidc_dialog, commands=["login"], state="*"
    )
    dp.register_message_handler(
        handle_email_microsoft_oidc_dialog, state=MicrosoftOIDCCredentialsState.email
    )
    dp.register_message_handler(
        handle_pwd_microsoft_oidc_dialog, state=MicrosoftOIDCCredentialsState.password
    )
