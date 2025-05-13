import sys
from typing import Literal


class UnsupportedSystemError(Exception):
    pass


async def get_operating_system() -> Literal['Windows', 'Linux', 'macOS', 'FreeBSD']:
    system = sys.platform.lower()
    if system.startswith('win'):
        return "Windows"
    elif system.startswith('linux'):
        return "Linux"
    elif system.startswith('darwin'):
        return "macOS"
    elif system.startswith('freebsd'):
        return 'FreeBSD'
    else:
        raise UnsupportedSystemError(f'Система {system} не поддерживается сервисом tuna')
