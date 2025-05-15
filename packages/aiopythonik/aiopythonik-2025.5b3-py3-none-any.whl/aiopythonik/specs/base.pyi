from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Optional, TypeVar

from pythonik.models.base import Response
from pythonik.specs.base import Spec

from ..rate_limiting import RateLimitHandler


T = TypeVar("T")


class AsyncSpecWrapper:
    _sync_spec: Any
    _executor: Optional[ThreadPoolExecutor]
    _rate_limit_handler: Optional[RateLimitHandler]

    def __init__(
        self,
        sync_spec: Any,
        executor: Optional[ThreadPoolExecutor] = None,
        rate_limit_handler: Optional[RateLimitHandler] = None,
    ) -> None:
        ...

    # Methods from test files
    async def get(self, resource_id: str, **kwargs) -> Response:
        ...

    async def method1(self, *args: Any, **kwargs: Any) -> Any:
        ...

    async def method2(self, *args: Any, **kwargs: Any) -> Any:
        ...

    async def method_with_default_args(
        self, arg1: str, arg2: Optional[int] = None, **kwargs: Any
    ) -> Any:
        ...

    async def get_resource(self, resource_id: str, **kwargs: Any) -> Any:
        ...

    async def create_resource(
        self, resource_data: Dict[str, Any], **kwargs: Any
    ) -> Any:
        ...

    async def delete_resource(self, resource_id: str, **kwargs: Any) -> Any:
        ...

    async def search(self, query: Dict[str, Any], **kwargs: Any) -> Any:
        ...


class AsyncSpec(AsyncSpecWrapper):

    def __init__(
        self,
        sync_spec: Spec,
        executor: Optional[Any] = None,
        rate_limit_handler: Optional[Any] = None,
    ) -> None:
        ...
