from celery import Celery

from src.core.config import ENV, CeleryConfig, CeleryConfigDocker

app = Celery("tasks")
app.config_from_object(CeleryConfig if ENV == "local" else CeleryConfigDocker)
app.autodiscover_tasks(["src.tgbot"])
