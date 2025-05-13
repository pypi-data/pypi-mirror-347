from datetime import datetime

from .base import TunaObject


class UserApiKey(TunaObject):
    """
    Этот объект представляет собой API-ключ пользователя

    Источник: https://my.tuna.am/swagger/swagger.json
    """

    created_at: datetime
    """Дата создания"""
    description: str
    """Описание"""
    expire_at: datetime
    """Дата истечения"""
    id: int
    """Идентификатор Apikey"""
    last_used_at: datetime
    """Дата последнего использования"""
    scopes: list[str]
    """Права доступа"""
    token: str
    """Токен"""
