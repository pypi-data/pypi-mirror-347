from typing import Type, TypeVar

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import text

from cores.configs.api_configs import Config

_host = Config.db_host
_username = Config.db_username
_password = Config.db_password
_database = Config.db_database
_engine = create_async_engine(
    (
        f"mysql+asyncmy://{_username}:{_password}@{_host}/{_database}"
        "?charset=utf8mb4"
    ),
    echo=Config.ECHO_DB_LOG,
    poolclass=NullPool,
    # isolation_level="READ UNCOMMITTED",
    # pool_pre_ping=True,
    # pool_size=5,
    # max_overflow=2
)
async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=_engine,  # type: ignore
    class_=AsyncSession,
    expire_on_commit=False,
)  # type: ignore

_mock_engine = create_async_engine(
    f"mysql+asyncmy://{_username}:{_password}@{_host}/mock_{_database}"
    "?charset=utf8mb4",
    echo=Config.ECHO_DB_LOG,
    pool_size=10,  # Số kết nối trong pool
    max_overflow=5,  # Số kết nối vượt quá pool_size
    pool_timeout=30,  # Thời gian chờ kết nối (giây)
    pool_recycle=3600,  # Tái chế kết nối sau 1 giờ
    # isolation_level="READ UNCOMMITTED",
    # pool_pre_ping=True,
    # pool_size=5,
    # max_overflow=2
)
mock_async_session = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=_mock_engine,  # type: ignore
    class_=AsyncSession,
    expire_on_commit=False,
)  # type: ignore

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///test_db.db"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
session_testing = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def get_db() -> AsyncSession:  # type: ignore
    async with async_session() as session:  # type: ignore
        try:
            yield session  # type: ignore
        finally:
            await session.close()


async def get_mock_db() -> AsyncSession:  # type: ignore
    async with mock_async_session() as session:  # type: ignore
        try:
            yield session  # type: ignore
        finally:
            await session.close()


async def get_db_testing() -> AsyncSession:  # type: ignore
    async with session_testing() as session:  # type: ignore
        try:
            yield session  # type: ignore
        finally:
            await session.close()


async def ping():
    try:
        async with _engine.connect() as conn:
            # Sử dụng `text` để thực hiện truy vấn
            await conn.execute(text("SELECT 1"))
            # Lấy kết quả để đảm bảo truy vấn đã được thực hiện
            return True
    except Exception as e:
        print(f"MySQL health check failed: {e}")
        return False


T = TypeVar("T")


# Base class cho SQLAlchemy ORM
class Base(DeclarativeBase):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_0900_ai_ci",
    }

    @classmethod
    def from_dict(cls, data: dict, exclude_none=True):
        if exclude_none:
            data = {k: v for k, v in data.items() if v is not None}
        return cls(**data)

    @classmethod
    def from_pydantic(cls, pydantic_model, exclude_none=True):
        data = pydantic_model.model_dump(exclude_none=exclude_none)
        return cls.from_dict(data)

    def to_pydantic(self, pydantic_model: Type[T]) -> T:
        """
        Chuyển đổi từ SQLAlchemy model sang Pydantic model.
        """
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return pydantic_model(**data)
