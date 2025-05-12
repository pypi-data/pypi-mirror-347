from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, List, Optional, TypeVar

from sqlalchemy import ScalarResult

from cores.model.paging import PagingDTO

# Define type variables
Entity = TypeVar("Entity")
Cond = TypeVar("Cond")
UpdateDTO = TypeVar("UpdateDTO")
CreateDTO = TypeVar("CreateDTO")
Cmd = TypeVar("Cmd")
Result = TypeVar("Result")
Query = TypeVar("Query")


# Query Repository Interface
class IQueryRepository(ABC, Generic[Entity, Cond]):
    @abstractmethod
    async def get(
        self,
        id: str | int,
        options=[],
        columns: list = [],
        with_trash: bool = False,
    ) -> Optional[Entity]:
        pass

    @abstractmethod
    async def get_by_ids(
        self,
        ids: list[int],
        options=[],
        columns: list = [],
        with_trash: bool = False,
    ) -> ScalarResult:
        pass

    @abstractmethod
    async def find_by_cond(
        self,
        cond: dict | list,
        options=[],
        columns: list = [],
        with_trash: bool = False,
    ) -> Optional[Entity]:
        pass

    @abstractmethod
    async def get_all_by_cond(
        self,
        cond: Cond = None,
        options=[],
        columns: list = [],
        with_trash: bool = False,
    ) -> list[Entity]:
        pass

    @abstractmethod
    async def get_list(
        self,
        cond: Cond,
        paging: PagingDTO,
        options=[],
        columns: list = [],
        with_trash: bool = False,
    ) -> List[Entity]:
        pass


# Command Repository Interface
class ICommandRepository(ABC, Generic[Entity, CreateDTO, UpdateDTO]):
    @abstractmethod
    async def insert(
        self, data: Entity | CreateDTO, with_commit=True, model_validate=True
    ) -> Entity:
        pass

    @abstractmethod
    async def update(
        self, id: str | int, data: UpdateDTO | dict, with_commit=True
    ) -> bool:
        pass

    @abstractmethod
    async def soft_update(
        self, old_entity: Entity, data: UpdateDTO | dict, with_commit=True
    ) -> Entity:
        pass

    @abstractmethod
    async def delete(
        self, id: str | int, is_hard: bool = False, with_commit=True
    ) -> bool:
        pass

    @abstractmethod
    async def update_or_create(
        self, defaults: dict[str, Any] | None = None, with_commit=True, **cond
    ) -> Entity:
        pass

    @abstractmethod
    def bulk_insert(self, entities: list[Entity]):
        pass

    @abstractmethod
    async def save_change(self) -> bool:
        pass

    @abstractmethod
    async def delete_by_condition(
        self, condition: dict, is_hard: bool = False, with_commit: bool = True
    ) -> bool:
        pass

    @abstractmethod
    async def update_by_condition(
        self, condition: dict, data: dict, with_commit: bool = True
    ) -> bool:
        pass


# Combined Repository Interface
class IRepository(
    IQueryRepository[Entity, Cond],
    ICommandRepository[Entity, CreateDTO, UpdateDTO],
    ABC,
):
    @abstractmethod
    async def list(
        self,
        cond: Cond,
        paging: PagingDTO,
        options=[],
        columns: list = [],
        with_trash: bool = False,
    ) -> List[Entity]:
        pass


class IMysqlRepository(
    IQueryRepository[Entity, Cond],
    ICommandRepository[Entity, CreateDTO, UpdateDTO],
    ABC,
):
    pass


# Command Handler Interface
class ICommandHandler(ABC, Generic[Cmd, Result]):
    @abstractmethod
    async def execute(self, command: Cmd) -> Result:
        pass


# Query Handler Interface
class IQueryHandler(ABC, Generic[Query, Result]):
    @abstractmethod
    async def query(self, query: Query) -> Result:
        pass


# Use Case Interface
class IUseCase(ABC, Generic[CreateDTO, UpdateDTO, Entity, Cond]):
    @abstractmethod
    async def create(self, data: CreateDTO) -> Entity:
        pass

    @abstractmethod
    async def get_detail(self, id: str | int) -> Optional[Entity]:
        pass

    @abstractmethod
    async def list(self, cond: Cond, paging: PagingDTO) -> list[Entity]:
        pass

    @abstractmethod
    async def update(self, id: str | int, data: UpdateDTO) -> Entity:
        pass

    @abstractmethod
    async def delete(self, id: str | int) -> bool:
        pass


# User Role Enum
class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"


# Token Payload Dataclass
@dataclass
class TokenPayload:
    id: str | int
    role: UserRole


# Token Payload Dataclass
@dataclass
class TokenPayloadV2:
    id: int = -1
    is_other_service: bool = False


# Requester Dataclass (extends TokenPayload)
@dataclass
class Requester(TokenPayload):
    pass


# Token Provider Interface
class ITokenProvider(ABC):
    @abstractmethod
    async def generate_token(self, payload: TokenPayload) -> str:
        pass

    @abstractmethod
    async def verify_token(self, token: str) -> Optional[TokenPayloadV2]:
        pass


# User Token Type
@dataclass
class UserToken:
    access_token: str
    refresh_token: str


# Token Introspect Result Type
@dataclass
class TokenIntrospectResult:
    payload: Optional[TokenPayloadV2] = None
    error: Optional[Exception] = None
    is_ok: bool = False
    user_token: Optional[str] = None


@dataclass
class CheckPermissionResult:
    can_action: bool = False
    user_id: int = -1


# Token Introspect Interface
class ITokenIntrospect(ABC):
    @abstractmethod
    async def introspect(self, token: str) -> TokenIntrospectResult:
        pass

    @abstractmethod
    async def check_access(
        cls,
        service_management_id: str,
        user_token: str,
        auth_token: str,
        method: str,
        url: str,
    ) -> TokenIntrospectResult:
        pass
