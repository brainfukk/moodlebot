from typing import Any, Dict, List, NoReturn, Optional, Type, Union

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.db.models import (
    BaseModel,
    MicrosoftOIDCCredentials,
    TelegramUser,
    TelegramUserMoodleSession,
)
from src.db.security import encrypt_password


class BaseRepo:
    model: Type[BaseModel]

    def __init__(self, session: Session) -> None:
        self.session = session

    def get(
        self, default: Optional[str] = None, **kwargs
    ) -> Union[BaseModel, NoReturn]:
        check_args = kwargs
        if default is not None:
            check_args = {default: kwargs[default]}
        return self.session.query(self.model).filter_by(**check_args).one()

    def create(self, instance: Optional[BaseModel] = None, **kwargs) -> BaseModel:
        if instance is None:
            instance = self.model(**kwargs)

        self.session.add(instance)
        self.session.commit()
        return instance

    def update(self, instance: BaseModel, values: Dict[str, Any]) -> BaseModel:
        for key, item in values.items():
            setattr(instance, key, item)
        self.session.commit()
        return instance

    def list(self) -> List[BaseModel]:
        return self.session.query(self.model).all()

    def get_or_create(self, default: Optional[str] = None, **kwargs) -> BaseModel:
        try:
            instance = self.get(default=default, **kwargs)
        except NoResultFound:
            instance = self.create(**kwargs)
        return instance

    def update_or_create(
        self,
        instance: Optional[BaseModel] = None,
        default: Optional[str] = None,
        **kwargs
    ) -> BaseModel:
        if instance is None:
            instance = self.get(default=default, **kwargs)

        if instance is None:
            instance = self.create(**kwargs)
            return instance
        return self.update(instance=instance, values=kwargs)

    def truncate(self):
        self.session.query(self.model).delete()
        self.session.commit()


class TelegramUserRepo(BaseRepo):
    model = TelegramUser


class MicrosoftOIDCCredentialsRepo(BaseRepo):
    model = MicrosoftOIDCCredentials

    def create(
        self, instance: Optional[MicrosoftOIDCCredentials] = None, **kwargs
    ) -> MicrosoftOIDCCredentials:
        if instance is None:
            kwargs["password"] = encrypt_password(password=kwargs["password"].encode())
            instance = self.model(**kwargs)
        else:
            instance.password = encrypt_password(instance.password.encode())
        return super().create(instance=instance)


class TelegramUserMoodleSessionRepo(BaseRepo):
    model = TelegramUserMoodleSession
