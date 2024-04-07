import aiohttp
from typing import Dict, Any, Union
from ..resources import SUCCESSFUL

class ApiHandler:
    def __init__(self, BASE: str):
        self.BASE = BASE

    async def request(self, endpoint: str, method: str = 'GET', html: bool = False, **kwargs: Any) -> Union[Dict[str, Any], str, int]:
        url = self.BASE + endpoint
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                response.raise_for_status()
                status_code: int = response.status

                if status_code != SUCCESSFUL:
                    return status_code
                
                if html == True:
                    return await response.text() 

                return await response.json() 

    async def get(self, endpoint: str, *, params: Dict[str, Any] = {}, **kwargs: Any) -> Union[Dict[str, Any], str, int]:
        return await self.request(endpoint, params=params, method='GET', **kwargs)

    async def post(self, endpoint: str, *, data: Dict[str, Any] = {}, **kwargs: Any) -> Union[Dict[str, Any], str, int]:
        return await self.request(endpoint, data=data, method='POST', **kwargs)

    async def put(self, endpoint: str, *, data: Dict[str, Any] = {}, **kwargs: Any) -> Union[Dict[str, Any], str, int]:
        return await self.request(endpoint, data=data, method='PUT', **kwargs)

    async def delete(self, endpoint: str, **kwargs: Any) -> Union[Dict[str, Any], str, int]:
        return await self.request(endpoint, method='DELETE', **kwargs)
