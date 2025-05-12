from datetime import datetime, timedelta
from typing import Dict, Optional, Union

import jwt
from cryptography.fernet import Fernet
from fastapi import Depends, Header, HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader, HTTPBearer
from jose import ExpiredSignatureError, JWTError
from pydantic import ValidationError

from cores.configs.api_configs import Config
from cores.repository.rpc.auth_client import AuthClient
from cores.repository.rpc.secret_key_menagement_client import (
    SecretKeyManagementClient,
)
from cores.repository.rpc.user_client import UserClient

SECURITY_ALGORITHM = "HS256"

# Security schemes
api_key_header_auth = APIKeyHeader(name="Api-key", auto_error=True)
service_id_header = APIKeyHeader(
    name="service-management-id",
    scheme_name="ServiceManagementId",
    description=f"Origin service id. Default: {Config.BASE_SERVICE_ID}",
    auto_error=True,
)
reusable_oauth2 = HTTPBearer(
    scheme_name="Authorization", description="JWT Token from Auth Service"
)


class TokenService:
    @staticmethod
    def generate_token(
        data: Dict, secret_key: str, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode["exp"] = expire
        return jwt.encode(to_encode, secret_key, algorithm=SECURITY_ALGORITHM)

    @staticmethod
    def decode_token(
        token: str, secret_key: str, verify_exp: bool = True
    ) -> Dict:
        try:
            options = {"verify_exp": False} if not verify_exp else {}
            return jwt.decode(
                token,
                secret_key,
                algorithms=[SECURITY_ALGORITHM],
                options=options,
            )
        except ExpiredSignatureError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": str(e), "require_refresh": True},
                headers={"WWW-Authenticate": "Bearer"},
            )
        except (JWTError, ValidationError) as e:
            raise HTTPException(
                status_code=(
                    status.HTTP_401_UNAUTHORIZED
                    if isinstance(e, JWTError)
                    else status.HTTP_403_FORBIDDEN
                ),
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    def decode_without_verification(token: str) -> Dict:
        try:
            return jwt.decode(
                token, key=None, options={"verify_signature": False}
            )
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    def create_token_pair(
        payload: Dict, private_key: str, public_key: str
    ) -> Dict[str, str]:
        access_payload = payload.copy()
        refresh_payload = payload.copy()
        access_payload["exp"] = datetime.utcnow() + timedelta(days=999999)
        refresh_payload["exp"] = datetime.utcnow() + timedelta(days=7)
        return {
            "access_token": jwt.encode(
                access_payload, public_key, algorithm=SECURITY_ALGORITHM
            ),
            "refresh_token": jwt.encode(
                refresh_payload, private_key, algorithm=SECURITY_ALGORITHM
            ),
        }


class AuthService:
    @staticmethod
    async def get_user_token(
        auth_token: str,
        service_management_id: str,
        user_token: str,
        target_service_id: str = Config.BASE_SERVICE_ID,
    ) -> bool | str:
        auth_client = AuthClient(auth_token)
        return await auth_client.validate_token(
            service_management_id, target_service_id, user_token
        )

    @staticmethod
    async def create_user_token(
        service_management_id: str, user_secret_key: Optional[str] = None
    ) -> str:
        if not user_secret_key:
            user_secret_key = (
                await SecretKeyManagementClient().get_secret_key()
            )
        return TokenService.generate_token(
            {"service_management_id": service_management_id}, user_secret_key
        )

    @staticmethod
    def create_auth_token(auth_secret: str) -> str:
        return TokenService.generate_token({}, auth_secret)


class EncryptionService:
    @staticmethod
    def encrypt_secret_key(encryption_key: str, secret_key: str) -> str:
        cipher = Fernet(encryption_key)
        return cipher.encrypt(secret_key.encode()).decode()

    @staticmethod
    def decrypt_secret_key(
        encryption_key: str, encrypted_secret_key: str
    ) -> str:
        cipher = Fernet(encryption_key)
        return cipher.decrypt(encrypted_secret_key.encode()).decode()


async def get_api_key(
    api_key_header: str = Security(api_key_header_auth),
) -> str:
    return api_key_header


async def check_access(
    request: Request,
    service_management_id: str = Depends(service_id_header),
    user_token: str = Header(...),
    auth_token=Depends(reusable_oauth2),
) -> None:
    user_token = await AuthService.get_user_token(
        auth_token.credentials, service_management_id, user_token
    )
    checked_result = await UserClient(user_token).check_permission(
        request.scope["root_path"] + request.scope["route"].path,
        request.method,
    )

    if checked_result.get("can_action", False):
        request.state.current_user_id = checked_result["user_id"]
        request.state.user_token = user_token
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập route này",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def validate_auth(
    request: Request,
    service_management_id: str = Depends(service_id_header),
    user_token: str = Header(...),
    auth_token=Depends(reusable_oauth2),
) -> bool:
    request.state.user_token = await AuthService.get_user_token(
        auth_token.credentials, service_management_id, user_token
    )
    return True


async def validate_token(
    request: Request, credentials=Depends(reusable_oauth2)
) -> int:
    result = await UserClient(credentials.credentials).validate_token()
    request.state.http_authorization_credentials = credentials
    if result and "id" in result:
        return int(result["id"])
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")


async def get_user_info(
    request: Optional[Request] = None, credentials=Depends(reusable_oauth2)
) -> Union[int, Dict]:
    result = await UserClient(credentials.credentials).get_me()
    if request:
        request.state.user_me = result
    return result


def check_access_token(access_token: str, secret_key: str) -> bool:
    try:
        payload = TokenService.decode_token(access_token, secret_key)
        return payload["exp"] > datetime.utcnow().timestamp()
    except HTTPException:
        return False
