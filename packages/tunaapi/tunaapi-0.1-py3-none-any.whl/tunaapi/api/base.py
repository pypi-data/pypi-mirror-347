import asyncio
import os
from subprocess import Popen
import json
from typing import List, Dict, Optional, Union

from httpx import Headers

from ..http_cli import BaseAPI
from .types import Tunnel, MemberShort
from .utils import get_operating_system


class BaseTunaAPI(BaseAPI):

    def __init__(self, api_key: str):
        self.url = 'https://my.tuna.am/'
        super().__init__()
        self.client.headers.update(
            Headers({'Authorization': f'Bearer {api_key}'})
        )
        self.processes: Dict[str, Popen[bytes]] = dict()

    async def get_tunnels(self, page_size: int, page: int) -> List[Tunnel]:
        """
        Используйте этот метод, чтобы получить список туннелей. При успешном выполнении вернётся список доступных туннелей.

        Источник: https://my.tuna.am/swagger/#/Tunnel/TunnelList

        :param page_size: Размер страницы
        :param page: Страница
        :return: Экземпляр ответа
        """

        return await self._get_tunnels(page_size, page)

    async def _get_tunnels(self, page_size: int, page: int) -> List[Tunnel]:
        from .methods import GetTunnels

        method = GetTunnels(page_size, page)
        response = await self._send_request(
            self.url + method.__endpoint__ + method.params,
            method.__method__
        )
        content: List[Dict] = json.loads(response._content.decode())
        tunnels = list()
        for tunnel in content:
            tunnel['owner'] = MemberShort(**tunnel['owner'])
            tunnels.append(Tunnel(**tunnel))
        return tunnels

    async def run_tunnel(self, proto: str, port: Optional[Union[int, str]] = None, wait: int = 1.5) -> Tunnel:
        """
        Используйте этот метод, чтобы запустить один туннель.

        :param proto: Протокол туннеля
        :param port: Порт туннеля
        :param wait: Время ожидания перед попыткой получения созданного туннеля; сделайте это значение больше, если у вас проблемы с интернетом
        :return: Экземпляр созданного туннеля
        """
        if proto in ['http', 'tcp']:
            assert port, 'Используя http или tcp, укажите порт для подключения'

        args = ['tuna', proto] + [str(port)] if port else []
        process = Popen(args)
        await asyncio.sleep(wait)                       # waiting for create tunnel
        tunnel = (await self.get_tunnels(5, 1))[-1]     # last started tunnel
        self.processes[tunnel.uid] = process

        return tunnel

    async def stop_tunnel(self, uid: Optional[str] = None, wait: int = 1.5) -> bool:
        """
        Используйте этот метод, чтобы остановить один туннель по его uid.
        :param uid: Uid туннеля
        :param wait: Время ожидания после удаления туннеля; сделайте это значение больше, если у вас проблемы с интернетом
        :return: True если процесс туннеля был найден и остановлен, иначе False
        """
        for tunnel_uid, proc in self.processes.copy().items():
            if tunnel_uid == uid:
                proc.kill()
                self.processes.pop(tunnel_uid)
                await asyncio.sleep(wait)
                return True
        return False

    async def stop_tuna(self, kill_session_only: bool = True):
        """
        Используйте этот метод, чтобы остановить все процессы tuna запущенные в данной сессии или все на устройстве.
        :param kill_session_only: Уничтожить только процессы данной сессии если True, иначе все на устройстве
        :return:
        """
        system = await get_operating_system()
        if kill_session_only:
            proc_ids = [str(proc.pid) for proc in self.processes.copy().values()]
            match system:
                case 'Windows':
                    cmd = 'taskkill /f' + ''.join([f' /PID {proc_id}' for proc_id in proc_ids])
                case 'masOS' | 'Linux' | 'FreeBSD':
                    cmd = 'kill -9 ' + ' '.join(proc_ids)
            self.processes.clear()
        else:
            match system:
                case 'Windows':
                    cmd = 'taskkill /f /IM tuna.exe'
                case 'masOS' | 'Linux' | 'FreeBSD':
                    cmd = 'killall tuna'
        os.system(cmd)
