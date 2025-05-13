from dataclasses import dataclass

from .base import TunaMethod
from ..types import Tunnel


@dataclass
class GetTunnels(TunaMethod):
    """
    Используйте этот метод, чтобы получить список туннелей

    Источник: https://my.tuna.am/swagger/#/Tunnel/TunnelList
    """

    __endpoint__ = 'v1/tunnels'
    __method__ = 'GET'
    __returning__ = list[Tunnel]

    page_size: int
    """Размер страницы"""   # Не точно
    page: int
    """Страница"""          # Не точно

    # if TYPE_CHECKING:
    #
    #     def __init__(
    #         self
    #     ) -> None:
    #
    #         super().__init__(...)