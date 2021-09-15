from src.celery_conf import app
from src.core.config import MICROSOFT_OIDC_EMAIL, MICROSOFT_OIDC_PWD
from src.db.database import session_scope
from src.services.oidc.auth import login

from .services.repository import (
    TelegramUserMoodleSessionRepo,
    TelegramUserRepo,
)


@app.task(name="authUser")
def auth_user(user_id: int):
    moodle_session: str = login(
        username=MICROSOFT_OIDC_EMAIL, password=MICROSOFT_OIDC_PWD
    )
    print(moodle_session + " MOODLESESSIONEPT")
    with session_scope() as session:
        repo = TelegramUserRepo(session=session)
        tg_user_moodle_repo = TelegramUserMoodleSessionRepo(session=session)
        user = repo.get(id=user_id)
        moodle_session_instance = tg_user_moodle_repo.update_or_create(
            telegram_user_id=user.id, hash=moodle_session, default="telegram_user_id"
        )
        print(moodle_session_instance)
