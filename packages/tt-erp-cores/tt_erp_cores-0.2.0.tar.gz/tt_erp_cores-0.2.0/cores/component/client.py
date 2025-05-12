import traceback
from io import BytesIO
from typing import Any

import httpx
from fastapi import HTTPException, status

from cores.configs.api_configs import Config
from cores.logger.logging import ApiLogger


class ClientBase:
    _app = None
    _base_url: str = ""
    _jwt_token: str = ""
    _headers: dict = {}

    async def set_jwt_token_and_headers(self, target_service_id: str):
        from cores.depends.authorization import AuthService

        self._jwt_token = AuthService.create_auth_token(Config.AUTH_SECRET_KEY)

        self._headers = {
            "service-management-id": Config.BASE_SERVICE_ID,
            "target-service-id": target_service_id,
            "user-token": await AuthService.create_user_token(
                Config.BASE_SERVICE_ID
            ),
        }

    async def curl_api(
        self,
        method="GET",
        uri="",
        body: dict = {},
        params: dict = {},
        response_type="json",
        external_headers: dict | None = None,
    ) -> Any:
        headers = self._prepare_headers(external_headers)
        link = self._base_url + uri
        client = httpx.AsyncClient(timeout=10, headers=headers, app=self._app)
        try:
            response = await self._make_request(
                client, method, link, body, params, headers
            )
            return await self._handle_response(
                response, response_type, link, method, params
            )
        except httpx.RequestError as exc:
            await self._log_error(exc, link, method, params, "RequestError")
        except Exception as exc:
            await self._log_error(exc, link, method, params, "Exception")
        finally:
            await self._close_client(client)

    def _prepare_headers(self, external_headers):
        headers = {"X-Requested-With": "XMLHttpRequest"}
        if self._jwt_token:
            headers["Authorization"] = "Bearer " + self._jwt_token
        if self._headers:
            headers.update(self._headers)
        if external_headers:
            headers.update(external_headers)
        return headers

    async def _make_request(
        self, client: httpx.AsyncClient, method, link, body, params, headers
    ):

        method = method.upper()

        if method == "GET":
            return await client.get(link, headers=headers, params=body)
        elif method == "POST":
            return await client.post(
                link, headers=headers, json=body, params=params
            )
        elif method == "PUT":
            return await client.put(
                link, headers=headers, json=body, params=params
            )
        elif method == "PATCH":
            return await client.patch(
                link, headers=headers, json=body, params=params
            )
        elif method == "DELETE":
            return await client.request(
                "delete", link, headers=headers, json=body
            )
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

    async def _handle_response(
        self, response, response_type, link, method, params
    ):
        if 500 > response.status_code > 202:
            ApiLogger.logging_curl(
                f"{link}, method: {method} failed with status {response.status_code}. "
                f"{response.text}"
            )

        if response_type == "binary":
            if response.status_code == 200:
                return BytesIO(response.content)
        else:
            return self._process_json_response(response)

    def _process_json_response(self, response):
        try:
            result = response.json()
            if isinstance(result, dict) and "status_code" not in result:
                result["status_code"] = response.status_code
            return result
        except httpx.DecodingError:
            ApiLogger.logging_curl(
                f"DecodingError for response: {response.text}"
            )
            raise

    async def _log_error(self, exc, link, method, params, error_type):
        error_message = f"{error_type} for {link}, method: {method}, params: {params} - {exc}"
        ApiLogger.logging_curl(error_message)

    async def _close_client(self, client):
        try:
            await client.aclose()
        except Exception:
            ApiLogger.logging_curl(
                f"Error closing client: {traceback.format_exc()}"
            )

    async def multipart_request(self, uri="", data=[], files=None):
        # timeout = httpx.TimeoutConfig(connect_timeout=5, read_timeout=None, write_timeout=5)
        headers = {
            "Authorization": "Bearer " + self._jwt_token,
            # 'Content-Type': 'application/json',
            "X-Requested-With": "XMLHttpRequest",
        }
        # print(headers)
        client = httpx.AsyncClient(timeout=10, headers=headers, app=self._app)
        try:
            r = None
            link = self._base_url + uri
            # print(link)
            r = await client.post(
                link, headers=headers, data=data, files=files
            )
            if r and r.status_code != 502:
                response = r.json()
                response["status_code"] = r.status_code
                return response
            else:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Service is unavailable.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except httpx.NetworkError as exc:
            ApiLogger.logging_curl(
                f"NetworkError for {exc.request.url} - {exc}"
            )
        except httpx.TimeoutException as exc:
            ApiLogger.logging_curl(
                f"TimeoutException for {exc.request.url} - {exc}"
            )
        except httpx.ProtocolError as exc:
            ApiLogger.logging_curl(
                f"ProtocolError for {exc.request.url} - {exc}"
            )
        except httpx.DecodingError as exc:
            ApiLogger.logging_curl(
                f"DecodingError for {exc.request.url} - {exc}"
            )
        except httpx.TooManyRedirects as exc:
            ApiLogger.logging_curl(
                f"TooManyRedirects for {exc.request.url} - {exc}"
            )
        except httpx.StreamError as exc:
            ApiLogger.logging_curl(f"StreamError for {link} - {exc}")
        except httpx.HTTPError as exc:
            ApiLogger.logging_curl(f"HTTP Exception - {link} {exc}")
        finally:
            await client.aclose()
        # catch Exception as e:

    async def curl_api_with_auth(
        self,
        _auth_init,
        method="GET",
        uri="",
        body=None,
        params=None,
        response_type="json",
        external_headers=None,
    ):
        await _auth_init()
        return await self.curl_api(
            method=method,
            uri=uri,
            body=body,
            params=params,
            response_type=response_type,
            external_headers=external_headers,
        )
