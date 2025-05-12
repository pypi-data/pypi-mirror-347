from cores.configs.api_configs import Config
from cores.interface.index import CheckPermissionResult, ITokenIntrospect
from cores.logger.logging import ApiLogger
from cores.repository.rpc.auth_client import AuthClient
from cores.repository.rpc.verify_token_rpc import TokenIntrospectRPCClient
from fastapi import Depends, Header, HTTPException, Request
from fastapi.security import (
    APIKeyHeader,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

service_id_header = APIKeyHeader(
    name="service-management-id",
    scheme_name="ServiceManagementId",
    description=f"""Origin service id to access the endpoints.
      Default: {Config.BASE_SERVICE_ID}""",
    auto_error=True,
)

reusable_oauth2 = HTTPBearer(
    scheme_name="Authorization", description="JWT Token from Auth Service."
)


async def auth_middleware(
    req: Request,
    user_token: str = Header(...),
):
    # 1. Introspect token
    introspector = TokenIntrospectRPCClient(user_token)
    introspected_result = await introspector.introspect()
    ApiLogger.debug(introspected_result)
    if not introspected_result.is_ok:
        raise HTTPException(
            401,
            detail=(
                introspected_result.error.detail
                if introspected_result.error.detail
                else "Unauthorized"
            ),
        )

    requester = introspected_result.payload

    # 2. Set requester to res.state
    req.state.requester = requester


async def check_access_middleware(
    req: Request,
    service_id: str = Depends(service_id_header),
    user_token: str = Header(...),
    auth_token=Depends(reusable_oauth2),
):
    # 1. Xác thực auth token từ request
    auth_client = AuthClient(auth_token.credentials)
    user_token = await auth_client.validate_token(
        service_id, Config.BASE_SERVICE_ID, user_token
    )

    # 2. Xác thực user token
    introspector = TokenIntrospectRPCClient(user_token)
    introspected_result = await introspector.introspect()
    if not introspected_result.is_ok:
        raise HTTPException(
            401,
            detail=(
                introspected_result.error.detail
                if introspected_result.error.detail
                else "Unauthorized"
            ),
        )

    requester = introspected_result

    # 3. Set requester to res.state
    req.state.requester = requester
    req.state.user_token = user_token


async def check_permission_middleware(
    req: Request,
    service_id: str = Depends(service_id_header),
    user_token: str = Header(...),
    auth_token: HTTPAuthorizationCredentials = Depends(reusable_oauth2),
):
    # 1. Xác thực auth token từ request
    auth_client = AuthClient(auth_token.credentials)
    user_token = await auth_client.validate_token(
        service_id, Config.BASE_SERVICE_ID, user_token
    )

    # 2. Xác thực quyền
    route = req.scope["root_path"] + req.scope["route"].path
    introspector = TokenIntrospectRPCClient(user_token)

    introspected_result = await introspector.check_permission(
        route, req.method
    )

    if not introspected_result.can_action:
        raise HTTPException(401, detail="Not permission")

    requester = introspected_result

    # 3. Set requester to res.state
    req.state.requester = requester
    req.state.user_token = user_token


_override_user_id = 1  # default


async def _override_check_access(req: Request):
    # ApiLogger.debug("check_access_middleware")
    requester = CheckPermissionResult(True, _override_user_id)

    # 3. Set requester to res.state
    req.state.requester = requester
    # req.state.user_token = ''
    return requester
