from datetime import datetime
from typing import Generic, Optional, TypeVar

from cores.model.base_model import CamelCaseModel

# Định nghĩa generic type cho Payload
Payload = TypeVar("Payload")


class DTOProps(CamelCaseModel):
    id: Optional[str] = None
    occurred_at: Optional[datetime] = None
    sender_id: Optional[str] = None


class AppEvent(CamelCaseModel, Generic[Payload]):
    event_name: str
    payload: Payload
    dto_props: DTOProps | None = None


# class AppEvent(Generic[Payload]):
#     def __init__(
#         self,
#         event_name: str,
#         payload: Payload,
#         dto_props: DTOProps | None = None,
#     ):
#         self._id: str = (
#             dto_props.id if dto_props and dto_props.id else str(uuid4())
#         )
#         self._occurred_at: datetime = (
#             dto_props.occurred_at
#             if dto_props and dto_props.occurred_at
#             else datetime.now()
#         )
#         self._sender_id: Optional[str] = (
#             dto_props.sender_id if dto_props else None
#         )
#         self._event_name: str = event_name
#         self._payload: Payload = payload

#     @property
#     def event_name(self) -> str:
#         """Lấy tên sự kiện"""
#         return self._event_name

#     @property
#     def id(self) -> str:
#         """Lấy ID của sự kiện"""
#         return self._id

#     @property
#     def occurred_at(self) -> datetime:
#         """Lấy thời điểm xảy ra sự kiện"""
#         return self._occurred_at

#     @property
#     def sender_id(self) -> Optional[str]:
#         """Lấy ID của người gửi (nếu có)"""
#         return self._sender_id

#     @property
#     def payload(self) -> Payload:
#         """Lấy dữ liệu payload của sự kiện"""
#         return self._payload

#     def plain_object(self) -> Dict[str, Any]:
#         """Chuyển đổi sự kiện thành dictionary"""
#         return {
#             "id": self._id,
#             "occurredAt": self._occurred_at.isoformat(),  # Chuyển datetime thành chuỗi ISO
#             "senderId": self._sender_id,
#             "eventName": self._event_name,
#             "payload": self._payload,
#         }


# # Ví dụ sử dụng
# if __name__ == "__main__":
#     # Ví dụ 1: Không dùng dto_props (sử dụng giá trị mặc định)
#     event1 = AppEvent(
#         event_name="user.created",
#         payload={"user_id": "123", "name": "Nguyen Van A"},
#     )
#     print("Ví dụ 1 - Không dùng dto_props:")
#     print(f"Tên sự kiện: {event1.event_name}")
#     print(f"ID (tự động): {event1.id}")
#     print(f"Thời điểm (hiện tại): {event1.occurred_at}")
#     print(f"Sender ID: {event1.sender_id}")
#     print(f"Payload: {event1.payload}")
#     print(f"Dạng dict: {event1.plain_object()}")
#     print("-" * 50)

#     # Ví dụ 2: Dùng dto_props để tùy chỉnh
#     custom_time = datetime(2023, 10, 15, 12, 0, 0)  # Thời điểm tùy chỉnh
#     event2 = AppEvent(
#         event_name="user.updated",
#         payload={"user_id": "456", "name": "Tran Thi B"},
#         dto_props={
#             "id": "custom-id-001",
#             "occurredAt": custom_time,
#             "senderId": "system-01",
#         },
#     )
#     print("Ví dụ 2 - Dùng dto_props:")
#     print(f"Tên sự kiện: {event2.event_name}")
#     print(f"ID (tùy chỉnh): {event2.id}")
#     print(f"Thời điểm (tùy chỉnh): {event2.occurred_at}")
#     print(f"Sender ID (tùy chỉnh): {event2.sender_id}")
#     print(f"Payload: {event2.payload}")
#     print(f"Dạng dict: {event2.plain_object()}")
