# Cores

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)

> Core utilities and base components for backend development

## Overview

`cores` là một thư viện cơ sở (core library) được thiết kế theo mô hình clean architecture, cung cấp các thành phần cơ bản cho việc phát triển ứng dụng backend. Module này giúp chuẩn hóa cách triển khai các tính năng chung và đảm bảo tính thống nhất trong toàn dự án.

## Cấu trúc thư mục

```
cores/
├── component/      # Base components (SQLAlchemy, validation,...)
├── logger/         # Logging system
├── middleware/     # API middlewares
├── utils/          # Utility functions
├── depends/        # Dependency injection
├── commands/       # CLI commands
├── model/          # Base models
├── repository/     # Repository pattern implementations
├── interface/      # Interface definitions
├── configs/        # Application configurations
├── transport/      # HTTP transport layer
├── enum/           # Shared enumerations
└── event/          # Event system
```

## Chi tiết các module

### `component/`

Cung cấp các thành phần cơ sở cho ứng dụng:

- **SQLAlchemy helpers**: Cấu hình kết nối, session management
- **Validators**: Các validation utilities
- **Data formatters**: Định dạng dữ liệu

```python
from cores.component.sqlalchemy import get_db, Base
```

### `logger/`

Hệ thống logging thống nhất:

- **API Logger**: Ghi log cho API requests/responses
- **Custom formatters**: Format log messages
- **Log levels**: Debug, Info, Warning, Error, Critical

```python
from cores.logger.logging import ApiLogger

ApiLogger.info("Operation successful")
ApiLogger.error("Error occurred", exc_info=True)
```

### `middleware/`

Các middleware cho API:

- **Authentication middleware**: Xác thực request
- **Error handling middleware**: Xử lý và format lỗi
- **Logging middleware**: Ghi log request/response

```python
from cores.middleware.auth import AuthMiddleware
from cores.middleware.error_handler import ErrorHandlerMiddleware

app.add_middleware(AuthMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
```

### `utils/`

Tiện ích và hàm hỗ trợ:

- **Date/time utilities**: Xử lý thời gian
- **String manipulation**: Xử lý chuỗi
- **Collection helpers**: Thao tác với list, dict

```python
from cores.utils.datetime import now_utc, format_datetime
from cores.utils.string import snake_to_camel
```

### `depends/`

Dependency injection system:

- **Service providers**: Cung cấp dependencies
- **Scoped dependencies**: Quản lý lifetime của dependencies

```python
from cores.depends.service import Depends
from cores.depends.providers import get_current_user

def endpoint(user = Depends(get_current_user)):
    # ...
```

### `model/`

Base models:

- **Entity base classes**: Mô hình domain
- **DTO base classes**: Data Transfer Objects
- **Response models**: API response wrappers

```python
from cores.model.base import BaseModel
from cores.model.response import DataResponse

class User(BaseModel):
    # ...

return DataResponse().success_response(data)
```

### `repository/`

Triển khai Repository pattern:

- **Base repository**: CRUD operations
- **Query repository**: Read operations
- **Command repository**: Write operations

```python
from cores.repository.base import BaseRepositorySQLAlchemy

class UserRepository(BaseRepositorySQLAlchemy):
    def __init__(self, session=Depends(get_db)):
        super().__init__(session, User)
```

### `interface/`

Định nghĩa interface:

- **Repository interfaces**: IRepository, IQueryRepository, ...
- **Service interfaces**: IUserService, ...
- **Protocol definitions**: Python protocols

```python
from cores.interface.repository import IRepository
from cores.interface.service import IUserService
```

### `configs/`

Cấu hình ứng dụng:

- **Environment settings**: Development, Production, Testing
- **API configurations**: Versioning, pagination, ...
- **Security settings**: Token, permissions, ...

```python
from cores.configs.api_configs import Config

base_url = Config.BASE_URL
```

### `transport/`

Transport layers:

- **HTTP controllers**: Base controller classes
- **WebSocket handlers**: WebSocket base
- **REST endpoints**: Base endpoint classes

```python
from cores.transport.http import BaseController
from cores.transport.websocket import WebSocketHandler
```

### `enum/`

Enumerations dùng chung:

- **Status enums**: Active/Inactive, Success/Error
- **Type enums**: UserType, ResourceType, ...

```python
from cores.enum.status import StatusEnum
from cores.enum.user import UserRoleEnum
```

### `event/`

Event system:

- **Event handlers**: Xử lý events
- **Event publishers**: Phát events
- **Event definitions**: Event models

```python
from cores.event.handler import EventHandler
from cores.event.publisher import EventPublisher
```

## Cách sử dụng

### Kiến trúc

Module `cores` được thiết kế theo clean architecture, phân tách rõ các layers:

- **Domain layer**: Models, interfaces
- **Application layer**: Use cases
- **Infrastructure layer**: Repositories, external services
- **Presentation layer**: API endpoints, controllers

### Import và sử dụng

```python
# Import base repository
from cores.repository.base import BaseRepositorySQLAlchemy

# Logger
from cores.logger.logging import ApiLogger

# Database
from cores.component.sqlalchemy import get_db, Base

# Config
from cores.configs.api_configs import Config

# Dependency injection
from cores.depends.service import Depends
```

### Ví dụ triển khai Repository

```python
from cores.repository.base import BaseRepositorySQLAlchemy
from cores.component.sqlalchemy import get_db
from cores.depends.service import Depends

class UserRepository(BaseRepositorySQLAlchemy):
    def __init__(self, session=Depends(get_db)):
        super().__init__(session, User)

    async def find_by_email(self, email: str):
        query = select(self.model).where(self.model.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
```

### Ví dụ triển khai API endpoint

```python
from fastapi import APIRouter
from cores.model.response import DataResponse
from cores.depends.service import Depends

router = APIRouter()

@router.get("/users/{user_id}")
async def get_user(user_id: int, user_repo = Depends(UserRepository)):
    user = await user_repo.get(user_id)
    return DataResponse().success_response(user)
```

## Lợi ích

1. **Thống nhất**: Đảm bảo chuẩn code trong toàn dự án
2. **Tái sử dụng**: Giảm code trùng lặp
3. **Dễ bảo trì**: Tách biệt rõ ràng các thành phần
4. **Dễ mở rộng**: Thêm tính năng mới mà không ảnh hưởng code hiện tại
5. **Testability**: Dễ dàng viết unit tests

## Đóng góp

Vui lòng đọc [CONTRIBUTING.md](CONTRIBUTING.md) để biết thêm về quy trình đóng góp.

## License

[MIT](LICENSE)
