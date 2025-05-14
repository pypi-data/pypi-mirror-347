from openremote.http import HttpClient
from typing import Any
from openremote.schemas.asset_object import AssetObject
import httpx


class Asset:
    __client: HttpClient

    def __init__(self, client: HttpClient):
        self.__client = client

    async def get_by_id(self, id: str) -> AssetObject | None:
        response = await self.__client.get(f'/api/master/asset/{id}')

        if response.is_error:
            return None

        return AssetObject(**response.json())

    async def query(self, query: dict[str, Any]) -> list[AssetObject]:
        response = await self.__client.post(f'/api/master/asset/query', json=query)

        print(response.status_code)

        return [AssetObject(**item) for item in response.json()]