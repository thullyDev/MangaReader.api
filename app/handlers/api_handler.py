import aiohttp
from typing import Dict, Any, Union

class ApiHandler:
    def __init__(self, BASE: str):
        self.BASE = BASE

    async def request(self, endpoint: str, method: str = 'GET', html: bool = False, **kwargs: Any) -> Union[Dict[str, Any], str]:
        url = self.BASE + endpoint
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                
                if html == True:
                    return await response.text() 

                return await response.json() 

    async def get(self, endpoint: str, *, params: Dict[str, Any] = {}, **kwargs: Any) -> Union[Dict[str, Any], str]:
        return await self.request(endpoint, params=params, method='GET')

    async def post(self, endpoint: str, *, data: Dict[str, Any] = {}, **kwargs: Any) -> Union[Dict[str, Any], str]:
        return await self.request(endpoint, data=data, method='POST')

    async def put(self, endpoint: str, *, data: Dict[str, Any] = {}, **kwargs: Any) -> Union[Dict[str, Any], str]:
        return await self.request(endpoint, data=data, method='PUT')

    async def delete(self, endpoint: str, **kwargs: Any) -> Union[Dict[str, Any], str]:
        return await self.request(endpoint, method='DELETE')
