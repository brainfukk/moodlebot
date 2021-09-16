import requests

from src.core.config import TELEGRAM_BOT_API_TOKEN

SEND_MESSAGE_URL: str = (
    "https://api.telegram.org"
    "/bot{api_token}"
    "/sendMessage?chat_id={chat_id}&text={text}"
)


def send_message(text: str, chat_id: int):
    with requests.Session() as session:
        url = SEND_MESSAGE_URL.format(
            api_token=TELEGRAM_BOT_API_TOKEN, chat_id=chat_id, text=text
        )
        response = session.get(url)
        return response
