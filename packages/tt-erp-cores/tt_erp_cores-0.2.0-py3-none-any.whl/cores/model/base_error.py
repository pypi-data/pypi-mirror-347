from typing import Any, Optional

from cores.utils.reason_phrases import ReasonPhrase
from cores.utils.status_codes import StatusCode
from starlette.exceptions import HTTPException as StarletteHTTPException

# Define status codes as constants
# class StatusCode:
#     FORBIDDEN = 403
#     CONFLICT = 409

# # Define reason messages as constants
# class ReasonStatusCode:
#     FORBIDDEN = 'Bad request error'
#     CONFLICT = 'Conflict error'

# Custom exception classes


class ErrorResponse(StarletteHTTPException):
    def __init__(
        self,
        message: Any = None,
        status: int = 500,
        headers: Optional[dict[str, Any]] = None,
    ):
        super().__init__(status_code=status, detail=message, headers=headers)


class ConflictRequestError(ErrorResponse):
    def __init__(self, message=ReasonPhrase.CONFLICT, status=StatusCode.CONFLICT):
        super().__init__(message, status)


class BadRequestError(ErrorResponse):
    def __init__(self, message=ReasonPhrase.BAD_REQUEST, status=StatusCode.BAD_REQUEST):
        super().__init__(message, status)


class NotfoundError(ErrorResponse):
    def __init__(self, message=ReasonPhrase.NOT_FOUND, status=StatusCode.NOT_FOUND):
        super().__init__(message, status)


class ForbiddenError(ErrorResponse):
    def __init__(self, message=ReasonPhrase.FORBIDDEN, status=StatusCode.FORBIDDEN):
        super().__init__(message, status)


class UnauthorizeError(ErrorResponse):
    def __init__(self, message=ReasonPhrase.UNAUTHORIZED, status=StatusCode.UNAUTHORIZED):
        super().__init__(message, status)
