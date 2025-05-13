from dataclasses import dataclass

from .base import TunaObject


@dataclass
class MemberShort(TunaObject):
    """
    Этот объект представляет собой Краткую информацию о пользователе

    Источник: https://my.tuna.am/swagger/swagger.json
    """
    active: bool
    """Признак активности"""
    avatar_url: str
    """Аватар"""
    email: str
    """Почта"""
    id: int
    """Идентификатор"""
    name: str
    """Имя"""
    role: str
    """Роль"""
