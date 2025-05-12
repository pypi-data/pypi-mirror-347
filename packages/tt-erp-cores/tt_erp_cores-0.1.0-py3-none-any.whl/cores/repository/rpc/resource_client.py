from cores.component.client import ClientBase
from cores.configs.api_configs import Config


class ResourceClient(ClientBase):
    async def _initialize(self):
        from cores.authorization.authorization_helper_v2 import (
            create_auth_token_for_be,
        )

        self._base_url = Config.RESOURCE_BASE_URL
        self._jwt_token = await create_auth_token_for_be(
            Config.SERVICE_MANAGEMENT_ID,
            Config.AUTH_SECRET_KEY,
            Config.BASE_URL,
            self._base_url,
        )
        return self

    async def upload(self, files=None, name=None, type=None):
        data = {"type": type, "name": name}
        return await self.curl_api_with_auth(
            self._initialize, "resources", data, files
        )

    async def get(self, page=1, size=15):
        params = {"page": page, "per_page": size}
        return await self.curl_api_with_auth(
            self._initialize, "GET", "api/resources/", params
        )

    async def find(self, resource_id):
        return await self.curl_api_with_auth(
            self._initialize, "GET", f"api/resources/{resource_id}"
        )
