import logging

from src.celery_conf import app
from src.core.tgbot.dialog import (
    AUTH_TASK_FINISHED_WORK_WITH_ERR,
    AUTH_TASK_GOT_MOODLE_SESSION,
    AUTH_TASK_SAVED_TO_DB_MOODLE_SESSION,
    AUTH_TASK_STARTED,
)
from src.db.database import session_scope
from src.services.oidc.auth import login
from src.tgbot.services.bot import send_message

from .services.repository import (
    TelegramUserMoodleSessionRepo,
    TelegramUserRepo,
)

logger = logging.getLogger(__name__)


@app.task(name="authUser")
def auth_user(user_id: int) -> None:
    with session_scope() as session:
        repo = TelegramUserRepo(session=session)
        tg_user_moodle_repo = TelegramUserMoodleSessionRepo(session=session)
        user = repo.get(id=user_id)

        try:
            send_message(
                chat_id=user.telegram_id,
                text=AUTH_TASK_STARTED,
            )
            credentials = repo.get_mcs_oidc_credentials(instance=user)
            moodle_session: str = login(
                username=credentials.email, password=credentials.password
            )
            send_message(
                chat_id=user.telegram_id,
                text=AUTH_TASK_GOT_MOODLE_SESSION.format(moodle_session),
            )

            tg_user_moodle_repo.update_or_create(
                telegram_user_id=user.id,
                hash=moodle_session,
                default="telegram_user_id",
            )
            send_message(
                chat_id=user.telegram_id,
                text=AUTH_TASK_SAVED_TO_DB_MOODLE_SESSION,
            )
        except Exception as err:
            logger.error(err)
            send_message(
                chat_id=user.telegram_id, text=AUTH_TASK_FINISHED_WORK_WITH_ERR
            )
