import logging
import os
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler


# Định nghĩa formatter tùy chỉnh với múi giờ Việt Nam
class VietnamTimeFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created) + timedelta(hours=7)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.isoformat()


# Định nghĩa handler tùy chỉnh để tạo tên file sao lưu
# theo định dạng ngày tháng
# (Custom handler for rotating log files with date-based backup names)
class CustomRotatingFileHandler(RotatingFileHandler):
    def __init__(self, base_filename, *args, **kwargs):
        self.base_filename = base_filename
        super().__init__(base_filename + ".log", *args, **kwargs)

    def doRollover(self):
        self.close()
        timestamp = datetime.now().strftime("%d-%m-%Y")
        backup_filename = f"{self.base_filename}-{timestamp}.log"
        self.rename_file(self.baseFilename, backup_filename)
        super().doRollover()

    def rename_file(self, old_filename, new_filename):
        if os.path.exists(old_filename):
            os.rename(old_filename, new_filename)


# Tạo thư mục logs nếu chưa tồn tại
os.makedirs("log", exist_ok=True)

# Formatter chi tiết cho mọi loại log
error_formatter = VietnamTimeFormatter(
    "%(asctime)s [%(module)s | %(levelname)s] @ "
    "%(pathname)s : %(lineno)d : %(funcName)s\n%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S%p",
)

# Tạo handlers với đường dẫn mới
info_handler = CustomRotatingFileHandler(
    "log/info", maxBytes=10485760, backupCount=5
)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(error_formatter)

error_handler = CustomRotatingFileHandler(
    "log/error", maxBytes=10485760, backupCount=5
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(error_formatter)

debug_handler = CustomRotatingFileHandler(
    "log/debug", maxBytes=10485760, backupCount=5
)
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(error_formatter)

success_handler = CustomRotatingFileHandler(
    "log/success", maxBytes=10485760, backupCount=5
)
success_handler.setLevel(logging.DEBUG)
success_handler.setFormatter(error_formatter)

curl_handler = CustomRotatingFileHandler(
    "log/curl_log", maxBytes=10485760, backupCount=5
)
curl_handler.setLevel(logging.ERROR)
curl_handler.setFormatter(error_formatter)

email_handler = CustomRotatingFileHandler(
    "log/err_email", maxBytes=10485760, backupCount=5
)
email_handler.setLevel(logging.ERROR)
email_handler.setFormatter(error_formatter)

task_handler = CustomRotatingFileHandler(
    "log/task", maxBytes=10485760, backupCount=5
)
task_handler.setLevel(logging.ERROR)
task_handler.setFormatter(error_formatter)

# Tạo loggers
general_logger = logging.getLogger("general")
general_logger.setLevel(logging.ERROR)
general_logger.addHandler(error_handler)

debug_logger = logging.getLogger("debug_config")
debug_logger.setLevel(logging.DEBUG)
debug_logger.addHandler(debug_handler)

success_logger = logging.getLogger("success_config")
success_logger.setLevel(logging.DEBUG)
success_logger.addHandler(success_handler)

info_logger = logging.getLogger("info_config")
info_logger.setLevel(logging.INFO)
info_logger.addHandler(info_handler)

curl_logger = logging.getLogger("curl_log")
curl_logger.setLevel(logging.ERROR)
curl_logger.addHandler(curl_handler)

email_logger = logging.getLogger("email")
email_logger.setLevel(logging.ERROR)
email_logger.addHandler(email_handler)

task_logger = logging.getLogger("task")
task_logger.setLevel(logging.ERROR)
task_logger.addHandler(task_handler)

# Ví dụ sử dụng các logger
logger = logging.getLogger(__name__)


class MyLogger:
    general_logger = general_logger
    debug_logger = debug_logger
    info_logger = info_logger


class ApiLogger:
    @staticmethod
    def error(*messages):
        for message in messages:
            general_logger.error(message, stacklevel=2)

    @staticmethod
    def debug(*messages, write_to_file=False):
        import json
        import os

        log_path = "debug.json"
        for message in messages:
            debug_logger.debug(message, stacklevel=2)
            if write_to_file:
                dir_name = os.path.dirname(log_path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)
                with open(log_path, "w", encoding="utf-8") as f:
                    try:
                        f.write(json.dumps(message, ensure_ascii=False) + "\n")
                    except Exception as e:
                        f.write(
                            json.dumps({"error": str(e), "raw": str(message)})
                            + "\n"
                        )

    @staticmethod
    def info(*messages):
        for message in messages:
            info_logger.info(message, stacklevel=2)

    @staticmethod
    def success(*messages):
        for message in messages:
            success_logger.info(message, stacklevel=2)

    @staticmethod
    def logging_curl(*messages):
        for message in messages:
            curl_logger.error(message, stacklevel=2)

    @staticmethod
    def logging_email(*messages):
        for message in messages:
            email_logger.error(message, stacklevel=2)

    @staticmethod
    def logging_task(*messages):
        for message in messages:
            task_logger.error(message, stacklevel=2)

    @staticmethod
    def debug_query(*queries):
        for query in queries:
            debug_logger.debug(
                str(query.compile(compile_kwargs={"literal_binds": True})),
                stacklevel=2,
            )
