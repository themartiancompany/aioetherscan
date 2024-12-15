from abc import ABC, abstractmethod


class BaseModule(ABC):
    def __init__(self, client):
        self._client = client

    @property
    @abstractmethod
    def _module(self) -> str:
        """Returns API module name."""

    async def _get(self, **params):
        return await self._client._http.get(params={**dict(module=self._module), **params})

    async def _post(self, **params):
        return await self._client._http.post(data={**dict(module=self._module), **params})
