from datetime import datetime

import jwt
from configs.service_config import ServiceConfig  # type: ignore
from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError
from pydantic import ValidationError

from cores.configs.api_configs import Config
from cores.depends.authorization import EncryptionService
from cores.interface.index import ITokenProvider, TokenPayload, TokenPayloadV2

SECURITY_ALGORITHM = "HS256"


class JwtTokenService(ITokenProvider):
    def __init__(self, secret_key: str, expires_in: str | int):
        self.secret_key = secret_key
        self.expires_in = expires_in

    async def generate_token(self, payload: TokenPayload) -> str:
        return jwt.encode(
            payload,
            self.secret_key,
            self.expires_in,
            algorithm=SECURITY_ALGORITHM,  # type: ignore
        )

    async def verify_token(self, token: str) -> TokenPayloadV2 | None:
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[SECURITY_ALGORITHM]
            )

            if "exp" in payload:
                self.check_token_expiry(payload)

            return TokenPayloadV2(
                is_other_service=(
                    payload["is_other_service"]
                    if "is_other_service" in payload
                    else False
                ),
                id=payload["id"],
            )

        except Exception:
            return None

    async def verify_token_v2(
        self, user_token: str, key_service=None
    ) -> TokenPayloadV2 | None:
        """
        Decode JWT token to get username => return payload
        """
        try:
            unverified_payload = jwt.decode(
                user_token, options={"verify_signature": False}, key=""
            )
            is_other_service = False
            user_id = 1
            if "service_management_id" in unverified_payload:
                payload = await self.handle_jwt_from_other_service(
                    key_service,
                    unverified_payload["service_management_id"],
                    user_token,
                )
                is_other_service = True
            elif "id" in unverified_payload:
                payload = await self.verify_token(user_token)
                if not payload:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User Token không hợp lệ",
                    )
                user_id = payload.id
            else:
                raise HTTPException(
                    status_code=403, detail="Token verified fail"
                )

            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token truyền vào đã cũ hoặc không hợp lệ",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return TokenPayloadV2(
                is_other_service=is_other_service,
                id=user_id,
            )

        except ExpiredSignatureError as e:
            self.handle_expired_token(e)
        except JWTError:
            self.handle_validation_error()
        except ValidationError:
            self.handle_validation_error()

    async def handle_jwt_from_other_service(
        self, key_service, service_management_id, token
    ):
        """
        Handle JWT errors and check if token is from another service.
        """
        try:
            service_secret_key = (
                await key_service.find_cached_secret_key_by_service(
                    service_management_id
                )
            )

            if service_secret_key is None:
                raise HTTPException(
                    status_code=422,
                    detail=f"Service {service_management_id} does not exist",
                )

            return self.decode_token_with_service_key(
                token, service_secret_key
            )
        except ExpiredSignatureError as e:
            self.handle_expired_token(e)
        except JWTError as e:
            return await self.handle_jwt_from_other_service(
                key_service, e, token
            )  # type: ignore
        except ValidationError:
            self.handle_validation_error()

    def handle_expired_token(self, error):
        """
        Handle expired token error.
        """
        res = {
            "message": str(error),
            "require_refresh": True,
        }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=res,
            headers={"WWW-Authenticate": "Bearer"},
        )

    def handle_validation_error(self):
        """
        Handle validation errors.
        """
        raise HTTPException(
            status_code=403,
            detail="User token không hợp lệ",
        )

    def check_token_expiry(self, payload):
        """
        Check if the token has expired.
        """
        if payload.get("exp") < datetime.now().timestamp():
            raise ExpiredSignatureError("Token has expired")

    def decode_token_with_service_key(self, token, service_secret_key):
        """
        Decode token with the service-specific secret key.
        """
        try:
            return jwt.decode(
                token,
                EncryptionService.decrypt_secret_key(
                    ServiceConfig.ENCRYPTION_KEY, service_secret_key
                ),
                algorithms=[SECURITY_ALGORITHM],
            )
        except JWTError:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="""Xác thực token từ BE Service
                  khác gọi đến không hợp lệ""",
                headers={"WWW-Authenticate": "Bearer"},
            )


jwt_provider = JwtTokenService(
    Config.access_token.USER_SECRET_KEY, Config.access_token.EXPIRES_IN
)

jwt_provider = JwtTokenService(
    Config.access_token.USER_SECRET_KEY, Config.access_token.EXPIRES_IN
)
