from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from .database import Base
from .utils import create_id_reference_string, create_table_name

UNKNOWN = "Unknown"


class BaseModel(Base):
    __abstract__ = True

    __created_at_name__ = "created_at"
    __updated_at_name__ = "updated_at"
    __datetime_func__ = func.now()

    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(
        __created_at_name__,
        TIMESTAMP(timezone=False),
        default=__datetime_func__,
        nullable=False,
    )
    updated_at = Column(
        __updated_at_name__,
        TIMESTAMP(timezone=False),
        default=__datetime_func__,
        onupdate=__datetime_func__,
        nullable=False,
    )

    def __repr__(self):
        columns = [col for col in self.__dict__.keys() if not col.startswith("_")]
        values_dict = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

        repr_string = "<{}({})>"
        attrs_string = ""

        for col_name in columns:
            attrs_string += "{}=".format(col_name) + "{" + col_name + "}, "
        attrs_string = attrs_string.format(**values_dict)
        return repr_string.format(self.__class__.__name__, attrs_string)


class TelegramUser(BaseModel):
    __tablename__ = create_table_name("telegram_users")

    telegram_id = Column(Integer, nullable=False)
    first_name = Column(String(length=255), nullable=True)
    last_name = Column(String(length=255), nullable=True)

    @property
    def full_name(self):
        fn = self.first_name if self.first_name else ""
        ln = self.last_name if self.last_name else ""
        return "{} {}".format(fn, ln).strip()


class MicrosoftOIDCCredentials(BaseModel):
    __tablename__ = create_table_name("micorosft_oidc_credentials")

    telegram_user_id = Column(
        Integer, ForeignKey(create_id_reference_string("telegram_users"))
    )
    email = Column(String(length=500))
    password = Column(String(length=500))

    telegram_user = relationship("TelegramUser", backref="microsoft_oidc_credentials")


class TelegramUserMoodleSession(BaseModel):
    __tablename__ = create_table_name("moodle_sessions")

    telegram_user_id = Column(
        Integer, ForeignKey(create_id_reference_string("telegram_users"))
    )
    hash = Column(String(length=255))

    telegram_user = relationship("TelegramUser", backref="moodle_sessions")
