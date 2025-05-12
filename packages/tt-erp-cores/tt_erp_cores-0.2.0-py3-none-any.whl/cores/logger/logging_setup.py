import asyncio
import json
import logging
from datetime import datetime

from cores.configs.api_configs import Config
from cores.logger.logging import ApiLogger


# Custom JSON Formatter
class JSONFormatter(logging.Formatter):
    def format(self, record):
        message_data = record.getMessage()
        # ApiLogger.error(message_data)
        message_data_as_dict: dict = json.loads(message_data)

        log_record = {
            "env": Config.APP_ENV,
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": message_data_as_dict.get("message", ""),
            "log_type": message_data_as_dict.get("log_type"),
            "user_id": message_data_as_dict.get("user_id", -1),
            "item_id": message_data_as_dict.get("item_id", -1),
            "processing_time": message_data_as_dict.get("processing_time", -1),
            "extra_info": json.dumps(message_data_as_dict.get("extra_info")),
            "logger_name": record.name,
            "service_id": Config.BASE_SERVICE_ID,  # Tên service hiện tại
            # "host": socket.gethostname(),
            # "path": record.pathname,
            # "line": record.lineno,
            # "module": record.module,
            # "function": record.funcName,
            # "exc_info": self.formatException(record.exc_info) if record.exc_info else None
        }
        # ApiLogger.error(log_record)
        return json.dumps(log_record)


class AsyncTCPLogHandler(logging.Handler):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.queue = asyncio.Queue()  # Hàng đợi cho log messages
        self.loop = asyncio.get_event_loop()  # Lấy event loop hiện tại
        self.task = self.loop.create_task(
            self.send_logs()
        )  # Bắt đầu task để gửi log

    async def send_logs(self):
        while True:
            log_message = await self.queue.get()  # Chờ đến khi có log message
            if log_message is None:  # Nếu nhận được None, dừng task
                break
            await self._send_log(log_message)  # Gửi log

    async def _send_log(self, log_message):
        try:
            reader, writer = await asyncio.open_connection(
                self.host, self.port
            )
            writer.write(log_message.encode("utf-8"))  # Ghi log vào socket
            await writer.drain()  # Đợi cho tới khi log được gửi
            writer.close()  # Đóng kết nối
        except Exception as e:
            ApiLogger.error(f"Error sending log: {e}")

    def emit(self, record):
        log_message = self.format(record) + "\n"
        # Đưa log vào hàng đợi, nhưng sử dụng await để chắc chắn coroutine được chờ
        asyncio.create_task(
            self.queue.put(log_message)
        )  # Đưa log vào hàng đợi

    async def async_close(self):
        # Đưa None vào hàng đợi để kết thúc task và chờ task hoàn thành
        await self.queue.put(None)
        await self.task

    def close(self):
        if not self.loop.is_closed():  # Kiểm tra xem loop đã bị đóng chưa
            try:
                self.loop.run_until_complete(
                    self.async_close()
                )  # Đóng một cách an toàn
            except RuntimeError as e:
                ApiLogger.error(
                    f"Failed to close AsyncTCPLogHandler cleanly: {e}"
                )
        super().close()


# Create AsyncTCPLogHandler
tcp_handler = AsyncTCPLogHandler(Config.FILEBEAT_HOST, Config.FILEBEAT_PORT)
tcp_handler.setLevel(logging.INFO)

# Set JSON Formatter for TCP handler
json_formatter = JSONFormatter()
tcp_handler.setFormatter(json_formatter)

# Create logger
logger = logging.getLogger("my_fastapi_app")
logger.addHandler(tcp_handler)
logger.setLevel(logging.INFO)


# ELK Logger for specific logs
class ELKLogger:
    @staticmethod
    def log(message, log_type="info", extra_info=None):
        log_message = json.dumps(
            {
                "message": message,
                "extra_info": extra_info or {},
                "log_type": log_type,  # Thêm loại log vào thông tin
            }
        )
        if log_type == "action":
            logger.info(log_message)
        elif log_type == "error":
            logger.error(log_message)
        else:
            logger.info(log_message)  # Mặc định là log info

    @staticmethod
    def log_action(
        action: str,
        current_user_id: int,
        entity_id: int,
        payload: dict = {},
        is_success: bool = True,
        error: str = None,
    ):
        tag = "[Success]" if is_success else "[Error]"
        message = f"{tag} {action}"
        extra_info = {"error": error, "payload": payload}

        log_message = json.dumps(
            {
                "message": message,
                "extra_info": extra_info or {},
                "log_type": "action",  # Thêm loại log vào thông tin
                "user_id": current_user_id,
                "item_id": entity_id,
            }
        )
        logger.info(log_message)

    @staticmethod
    def log_processing_time(message, processing_time, extra_info=None):
        log_message = json.dumps(
            {
                "message": message,
                "extra_info": extra_info or {},
                "processing_time": processing_time,
                "log_type": "processing_time",  # Thêm loại log vào thông tin
            }
        )
        logger.info(log_message)


# # Example usage for action log
# def log_action(action, user_id, item_id):
#     ELKLogger.log(f"Action performed: {action}", log_type="action", extra_info={
#         "action": action,
#         "user_id": user_id,
#         "item_id": item_id
#     })

# def log_processing_time(action_name: str):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             start_time = datetime.utcnow()  # Bắt đầu tính thời gian
#             result = await func(*args, **kwargs)
#             end_time = datetime.utcnow()  # Kết thúc tính thời gian
#             processing_time = (end_time - start_time).total_seconds()
#             ELKLogger.log(f"Processing time for {action_name}: {processing_time}s", log_type="processing_time")
#             return result
#         return wrapper
#     return decorator

# def log_action(action_name: str):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             # Lấy request từ args (giả sử request luôn là tham số đầu tiên hoặc có trong kwargs)
#             request: Request = kwargs.get('request') or next((arg for arg in args if isinstance(arg, Request)), None)
#             if request:
#                 route_name = request.scope["path"]
#             else:
#                 route_name = "unknown"
#             # Lấy current_user_id từ kwargs (nếu có)
#             current_user_id = kwargs.get('user_id', 'Unknown User')
#             ELKLogger.log(f"Action performed: {action_name}", log_type="action", extra_info={
#                 "action": route_name,
#                 "user_id": current_user_id,
#             })
#             result = await func(*args, **kwargs)
#             return result
#         return wrapper
#     return decorator
