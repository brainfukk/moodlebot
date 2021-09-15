from aiogram.dispatcher.filters.state import State, StatesGroup


class MicrosoftOIDCCredentialsState(StatesGroup):
    email = State()
    password = State()
