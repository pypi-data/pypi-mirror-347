from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from .base import TunaObject
from . import MemberShort


@dataclass
class Tunnel(TunaObject):
    """
    Этот объект представляет собой Туннель

    Источник: https://my.tuna.am/swagger/swagger.json
    """

    active: bool
    """Признак текущей активности"""
    client_name: str
    """Имя клиента"""
    client_version: int
    """Версия клиента"""
    forwards_to: str
    """Перенаправление в"""
    id: int
    """ID туннеля"""
    location: str
    """Локация"""
    os: str
    """OS клиента"""
    owner: MemberShort
    """Владелец туннеля"""
    protocol: str
    """Протокол"""
    protocol_handler: str
    """Обработчик протокола"""
    public_url: str
    """Публичный URL адрес"""
    started_at: datetime
    """Дата запуска"""
    uid: str
    """UID туннеля"""
    created_at: datetime
    """Дата создания"""
    deleted_at: Optional[datetime] = None
    """Дата удаления"""
