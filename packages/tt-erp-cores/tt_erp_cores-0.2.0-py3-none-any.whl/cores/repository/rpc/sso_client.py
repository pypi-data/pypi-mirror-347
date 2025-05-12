from cores.component.client import ClientBase
from cores.configs.api_configs import Config


class SSOClient(ClientBase):
    async def _initialize(self):
        from cores.authorization.authorization_helper_v2 import (
            create_auth_token_for_be,
        )

        self._base_url = Config.SSO_BASE_URL
        self._jwt_token = await create_auth_token_for_be(
            Config.SERVICE_MANAGEMENT_ID,
            Config.AUTH_SECRET_KEY,
            Config.BASE_URL,
            self._base_url,
        )
        return self

    async def check_is_login(self):
        return await self.curl_api("GET", "is-login")

    async def get_info(self):
        return await self.curl_api("GET", "info")

    async def refresh_token(self):
        return await self.curl_api("GET", "refresh-token")
