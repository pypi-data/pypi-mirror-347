from .exceptions import UnexpectedMethodError

from httpx import AsyncClient, Response


class BaseAPI:

    def __init__(self):

        self.client = AsyncClient(
            headers={'Accept': 'application/json',
                     'Content-Type': 'application/json'},
            verify=False
        )

    async def _send_request(self, url: str, method: str, **kwargs) -> Response:
        match method:
            case 'GET':
                response = await self.client.get(url, **kwargs)
            case 'POST':
                response = await self.client.post(url, **kwargs)
            case 'PUT':
                response = await self.client.put(url, **kwargs)
            case 'DELETE':
                response = await self.client.delete(url, **kwargs)
            case _:
                raise UnexpectedMethodError(method)
        return response
