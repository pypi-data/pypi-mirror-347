import json
import os
import random
import re
import time
import unicodedata
import uuid
from datetime import datetime, timedelta
from functools import wraps
from typing import Any
from urllib.parse import urlparse

import jwt
import pandas as pd
from decouple import config
from fastapi import HTTPException


def to_camel_case(data):
    if isinstance(data, dict):
        return {
            "".join(
                word.capitalize() if i > 0 else word
                for i, word in enumerate(key.split("_"))
            ): to_camel_case(value)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [to_camel_case(item) for item in data]
    return data


def str_to_bool(value: str) -> bool:
    """Chuyển đổi chuỗi thành boolean"""
    # Dictionary để ánh xạ các giá trị chuỗi thành boolean
    bool_map = {
        "true": True,
        "1": True,
        "yes": True,
        "false": False,
        "0": False,
        "no": False,
    }

    # Chuyển đổi chuỗi đầu vào thành chữ thường và loại bỏ khoảng trắng
    value = value.strip().lower()

    # Sử dụng dictionary để lấy giá trị boolean
    if value in bool_map:
        return bool_map[value]
    else:
        raise ValueError(f"Invalid boolean string: {value}")


def get_uuid_id():
    return str(uuid.uuid4())


def with_err_log(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # my_header = request.headers.get('my-header')
        # print(request.headers)
        # my_header will be now available in decorator
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)

    return wrapper


async def get_admin():
    from cores.repository.rpc.user_client import UserClient

    admin = await UserClient().search("email", config("ADMIN_MAIL"))
    return admin


def sqlachemy_obj_to_dict(obj):
    dictret = obj.__dict__
    if "_sa_instance_state" in dictret:
        dictret.pop("_sa_instance_state", None)
    if "created_at" in dictret:
        dictret.pop("created_at", None)
    if "updated_at" in dictret:
        dictret.pop("updated_at", None)
    if "deleted_at" in dictret:
        dictret.pop("deleted_at", None)
    return dictret


def clean_str_to_import(data):
    if type(data) is not str:
        data = str(data)
    data = data.strip()
    data = data.replace("\n", ". ")
    data = data.replace('"', "'")
    return data


def get_current_time_as_int() -> int:
    now = datetime.now()
    current_time = now.timestamp()
    return int(current_time)


def convert_datetime_to_timestamp(y, m, d, h=0, i=0, s=0) -> int:
    now = datetime(y, m, d, h, i, s)
    current_time = now.timestamp()
    return int(current_time)


def check_is_roman(subject):
    pattern = "M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})"
    if subject:
        if re.fullmatch(pattern, subject):
            return True
        return False


def number_to_roman(number):
    list_map = {
        "XL": 40,
        "X": 10,
        "IX": 9,
        "V": 5,
        "IV": 4,
        "I": 1,
    }
    number = int(number)
    return_value = ""
    while number > 0:
        for roman, num_int in list_map.items():
            if number >= num_int:
                number = number - num_int
                return_value = return_value + roman
                break
    return return_value


def open_file_as_root_path(file_path):
    # root_path = os.path.dirname(__file__)

    abs_file_path = os.path.join(path_root, file_path)
    return open(abs_file_path, "rb")


def write_to_json(file_path, content):

    abs_file_path = os.path.join(path_root, file_path)
    f = open(abs_file_path + "/output.json", "w")
    f.write(content)
    print(abs_file_path)


def object_to_dict(obj, with_relation=False, exclude_relation=[], found=None):
    from sqlalchemy.orm import class_mapper

    if found is None:
        found = set()
    mapper = class_mapper(obj.__class__)
    columns = [column.key for column in mapper.columns]
    get_key_value = lambda c: (
        (c, getattr(obj, c).isoformat())
        if isinstance(getattr(obj, c), datetime)
        else (c, getattr(obj, c))
    )
    out = dict(map(get_key_value, columns))
    if with_relation:
        for name, relation in mapper.relationships.items():
            if relation not in found and str(relation) not in exclude_relation:
                found.add(relation)
                related_obj = getattr(obj, name)
                if related_obj is not None:
                    if relation.uselist:
                        out[name] = [
                            object_to_dict(
                                child, with_relation, exclude_relation, found
                            )
                            for child in related_obj
                        ]
                    else:
                        out[name] = object_to_dict(
                            related_obj, with_relation, exclude_relation, found
                        )
    return out


def no_accent_vietnamese(s):
    s = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", s)
    s = re.sub(r"[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]", "A", s)
    s = re.sub(r"[èéẹẻẽêềếệểễ]", "e", s)
    s = re.sub(r"[ÈÉẸẺẼÊỀẾỆỂỄ]", "E", s)
    s = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", s)
    s = re.sub(r"[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]", "O", s)
    s = re.sub(r"[ìíịỉĩ]", "i", s)
    s = re.sub(r"[ÌÍỊỈĨ]", "I", s)
    s = re.sub(r"[ùúụủũưừứựửữ]", "u", s)
    s = re.sub(r"[ƯỪỨỰỬỮÙÚỤỦŨ]", "U", s)
    s = re.sub(r"[ỳýỵỷỹ]", "y", s)
    s = re.sub(r"[ỲÝỴỶỸ]", "Y", s)
    s = re.sub(r"[Đ]", "D", s)
    s = re.sub(r"[đ]", "d", s)
    s = s.replace(" ", "")
    return s.lower()


def convert_tz_utc_to_vietnamese(dt):
    import datetime

    time_change = datetime.timedelta(hours=7)
    return dt + time_change


def create_storage_dir():
    storage_name = "storages"
    storage_path = "/" + storage_name + "/"
    if not os.path.isdir(storage_name):
        os.mkdir(storage_name)

    directory = os.getcwd() + storage_path

    prefix_dir = os.path.join(
        directory,
    )

    if not os.path.isdir(prefix_dir):
        os.mkdir(prefix_dir)

    mydir = os.path.join(directory, datetime.now().strftime("%Y-%m-%d"))

    if not os.path.isdir(mydir):
        os.mkdir(mydir)

    return mydir


def get_hashed_file_name(extension):
    return uuid.uuid4().hex + f".{extension}"


def generate_short_uuid():
    # Get the current timestamp
    timestamp = int(time.time())

    # Generate a random component
    random_component = random.randint(0, 99999999)

    # Combine timestamp and random component
    short_uuid = f"{timestamp:08x}{random_component:08x}"

    return short_uuid[:8]


def convert_base_url_to_ip(base_url):
    base_url = urlparse(base_url)
    return f"{base_url.hostname}:{base_url.port}"


def create_jwt_token(secret_key, payload, expires_delta: timedelta = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=999999)

    payload.update({"exp": expire})
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def slugify(value):
    # Chuyển đổi thành Unicode tổ hợp bình thường
    value = unicodedata.normalize("NFKD", value)
    # Chuyển đổi thành chuỗi ASCII
    value = value.encode("ascii", "ignore").decode("ascii")
    # Chuyển đổi thành chữ thường
    value = value.lower()
    # Loại bỏ các ký tự không phải chữ cái, chữ số hoặc khoảng trắng
    value = re.sub(r"[^\w\s-]", "", value)
    # Thay thế khoảng trắng hoặc dấu gạch ngang liền kề bằng một dấu gạch ngang duy nhất
    value = re.sub(r"[-\s]+", "-", value)
    # Loại bỏ dấu gạch ngang ở đầu và cuối chuỗi
    value = value.strip("-")
    return value


# async def fake_fe_token(user_id):
def load_cache_keys():
    CACHE_KEYS_FILE = "cache_keys.json"
    """Load các cache key từ file, nếu file không tồn tại thì trả về danh sách trống."""
    cache_keys_file = Path(CACHE_KEYS_FILE)

    if cache_keys_file.exists():
        with open(CACHE_KEYS_FILE, "r") as f:
            return json.load(f)
    return []


# Cắt bớt các field có nội dung quá dài
def truncate_message(msg, max_length=100) -> dict:
    truncated_msg = {}
    for key, value in msg.items():
        if isinstance(value, str) and len(value) > max_length:
            truncated_msg[key] = value[:max_length] + "..."
        else:
            truncated_msg[key] = value
    return truncated_msg


def create_html_file(file_name, content):
    # Đường dẫn tới thư mục gốc và tên file HTML
    file_path = f"./{file_name}.html"

    # Mở file và ghi nội dung vào
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    print(
        f"File HTML '{file_name}.html' đã được tạo thành công tại thư mục gốc."
    )


def get_value(
    row: pd.Series,
    column: str,
    dtype: Any = str,
    default: Any = None,
):
    """Lấy giá trị từ row và ép kiểu dữ liệu phù hợp"""
    value = row[column] if column in row and pd.notna(row[column]) else default

    # Loại bỏ space từ giá trị
    value = str(value).strip() if value is not None else value

    if dtype == str:
        return value

    try:
        return dtype(value)
    except ValueError:
        return default


def normalize_text(text: str) -> str:
    """Chuẩn hóa text để tăng độ chính xác tìm kiếm"""
    text = text.lower().strip()

    # Xóa khoảng trắng thừa
    text = re.sub(r"\s+", " ", text)

    # Chuyển đổi giữa 'y' <=> 'i' trong từ có dấu
    text = re.sub(r"y(?=[^a-z])", "i", text)
    text = re.sub(r"i(?=[^a-z])", "y", text)

    return text


KEYWORD_TO_ASSET = {
    "news": "NEWS",
    "bai bao": "NEWS",
    "tin tuc": "NEWS",
    "bao": "NEWS",
    "bai viet": "NEWS",
    "thong tin": "NEWS",
    "article": "NEWS",
    "report": "NEWS",
    "story": "NEWS",
    "image": "IMAGE",
    "hinh anh": "IMAGE",
    "anh": "IMAGE",
    "tam hinh": "IMAGE",
    "buc anh": "IMAGE",
    "hinh": "IMAGE",
    "picture": "IMAGE",
    "photo": "IMAGE",
    "pic": "IMAGE",
    "video": "VIDEO",
    "clip": "VIDEO",
    "phim": "VIDEO",
    "doan phim": "VIDEO",
    "movie": "VIDEO",
}


def remove_accents(text: str) -> str:
    """Loại bỏ dấu tiếng Việt để chuẩn hóa dữ liệu"""
    return (
        "".join(
            c
            for c in unicodedata.normalize("NFD", text)
            if unicodedata.category(c) != "Mn"
        )
        .lower()
        .strip()
    )


def detect_asset_type(user_input: str) -> str | None:
    """Tra cứu danh mục từ từ khóa, tối ưu với dict"""
    return KEYWORD_TO_ASSET.get(user_input.lower().strip(), user_input)


def zip_files(file_paths, output_zip):
    import zipfile

    try:
        with zipfile.ZipFile(output_zip, "w") as zipf:
            for file in file_paths:
                zipf.write(file, arcname=file.split("/")[-1])
    except Exception as e:
        print(f"Error zipping files: {e}")
        return False
    finally:
        return True


def convert_mongo_id(doc: dict) -> dict:
    """Chuyển _id của document MongoDB thành id (str), loại bỏ _id."""
    if doc is None:
        return doc
    doc = dict(doc)
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc
