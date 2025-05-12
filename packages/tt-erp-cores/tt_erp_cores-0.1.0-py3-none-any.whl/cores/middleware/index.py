import json

# from starlette.middleware import Middleware
import time
import traceback
import uuid
from collections import defaultdict

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from cores.configs.api_configs import Config
from cores.logger.logging import ApiLogger
from cores.logger.logging_setup import ELKLogger


async def log_info(request: Request) -> dict:
    try:
        body = await request.json()
    except json.JSONDecodeError:
        body = await request.body()
        body = body.decode("utf-8")  # Chuyển đổi sang chuỗi

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # # Log thông tin request
    # method = request.method
    # path = request.url.path
    # query_params = dict(request.query_params)
    # ApiLogger.info(
    #     f"Request ID: {request_id} | Method: {method} | Path: {path} | "
    #     f"Query Params: {json.dumps(query_params)} | Body: {body}"
    # )
    # ELKLogger.log(
    #     f"Request ID: {request_id} | Method: {method} | Path: {path} | "
    #     f"Query Params: {json.dumps(query_params)} | Body: {body}",
    #     log_type='info'
    # )

    return request


async def log_processing_time(request_id: str, start_time: float):
    end_time = time.time()  # Ghi nhận thời gian kết thúc xử lý
    processing_time = end_time - start_time  # Tính toán thời gian xử lý

    # Log thời gian xử lý
    ApiLogger.info(
        f"Request ID: {request_id} | Processing Time: {processing_time:.4f} seconds"
    )


async def catch_exceptions_middleware(request: Request, call_next):
    request_id = (
        request.state.request_id
        if hasattr(request.state, "request_id")
        else None
    )
    try:
        response = await call_next(request)
        if request_id:
            response.headers["X-Request-ID"] = request_id
        return response
    except Exception as e:
        # Ghi lại lỗi vào log
        ApiLogger.error(
            f"\nRequest ID: {request_id} {traceback.format_exc()} "
        )
        ELKLogger.log(
            message=f"Request ID: {request_id}. Error: {str(e)} ",
            log_type="error",
        )

        # Nếu môi trường là local, trả về chi tiết lỗi
        if Config.APP_ENV != "production":
            formatted_traceback = traceback.format_exc().splitlines()
            err_detail = {
                "request_id": request_id,
                "detail": str(e),
                "traceback": formatted_traceback,
            }
            return JSONResponse(err_detail, status_code=500)

        # Nếu không, trả về thông báo lỗi chung chung
        return JSONResponse(
            {"detail": "Internal server error"}, status_code=500
        )


# Hàm middleware để log thời gian xử lý
async def log_processing_time(request: Request, call_next):
    start_time = time.time()  # Ghi nhận thời gian bắt đầu xử lý

    response = await call_next(request)

    processing_time = time.time() - start_time  # Tính toán thời gian xử lý

    # Log thời gian xử lý
    request_id = (
        request.state.request_id
        if hasattr(request.state, "request_id")
        else None
    )
    # ApiLogger.info(f"Request ID: {request_id} | Path: {request.url.path} | Processing Time: {processing_time:.4f} seconds")
    if processing_time >= 0.5:
        ELKLogger.log_processing_time(
            f"Request ID: {request_id} | Path: {request.url.path} | Processing Time: {processing_time:.4f} seconds",
            processing_time=processing_time,
        )
    return response


def integrate_sentry():
    # sentry
    if Config.SENTRY_ENABLE:
        import sentry_sdk

        sentry_sdk.init(
            dsn=Config.SENTRY_DNS,
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0,
        )


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, limit: int, period: int):
        super().__init__(app)
        self.limit = limit
        self.period = period
        self.visits = defaultdict(
            lambda: defaultdict(list)
        )  # Khởi tạo nested defaultdict

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        route_path = request.url.path
        now = time.time()

        # Xóa timestamps bên ngoài thời gian giới hạn
        self.visits[client_ip][route_path] = [
            ts
            for ts in self.visits[client_ip][route_path]
            if ts > now - self.period
        ]

        # Kiểm tra số lần truy cập
        if len(self.visits[client_ip][route_path]) >= self.limit:
            raise HTTPException(status_code=429, detail="Too many requests")

        # Thêm timestamp mới
        self.visits[client_ip][route_path].append(now)

        response = await call_next(request)
        return response
