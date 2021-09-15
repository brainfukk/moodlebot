from decouple import config

# ENV type
ENV = config("ENV", cast=str)

# Microsoft references
MICROSOFT_OIDC_URL = config("MICROSOFT_OIDC_URL", cast=str)
MICROSOFT_OIDC_EMAIL = config("MICROSOFT_OIDC_EMAIL", cast=str)
MICROSOFT_OIDC_PWD = config("MICROSOFT_OIDC_PWD", cast=str)

# Database configs
DATABASE_URL = config("DATABASE_URL", cast=str)
TABLES_PREFIX = config("TABLES_PREFIX", cast=str)

# Security
SECRET_KEY = config("SECRET_KEY", cast=str)

# Telegram Bot
TELEGRAM_BOT_API_TOKEN = config("TELEGRAM_BOT_API_TOKEN", cast=str)
TELEGRAM_BOT_ADMIN_IDS = config("TELEGRAM_BOT_ADMIN_IDS", cast=str).split(",")
TELEGRAM_BOT_USE_REDIS = config("TELEGRAM_BOT_USE_REDIS", cast=bool)

# Celery
CELERY_BACKEND_URL = config("CELERY_BACKEND_URL", cast=str)


class CeleryConfig:
    broker_url = CELERY_BACKEND_URL
    backend = CELERY_BACKEND_URL
    RESULT_BACKEND = CELERY_BACKEND_URL
    ACCEPT_CONTENT = ["application/json"]
    RESULT_SERIALIZER = "json"
    TASK_SERIALIZER = "json"
    TIMEZONE = "Asia/Almaty"


class CeleryConfigDocker:
    broker_url = "redis://redis:6379/0"
    backend = "redis://redis:6379/0"
    RESULT_BACKEND = "redis://redis:6379/0"
    ACCEPT_CONTENT = ["application/json"]
    RESULT_SERIALIZER = "json"
    TASK_SERIALIZER = "json"
    TIMEZONE = "Asia/Almaty"
