from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Optional, Union

from pythonik.models.base import Response
from pythonik.specs.collection import Collection

from .._pythonik_patches import CollectionSpec
from ..rate_limiting import RateLimitHandler


class AsyncCollectionSpec:
    _sync_spec: CollectionSpec
    _executor: Optional[ThreadPoolExecutor]
    _rate_limit_handler: Optional[RateLimitHandler]

    def __init__(
        self,
        sync_spec: CollectionSpec,
        executor: Optional[Any] = None,
        rate_limit_handler: Optional[Any] = None,
    ) -> None:
        ...

    async def get(self, collection_id: str, **kwargs) -> Response:
        ...

    async def fetch(self, **kwargs) -> Response:
        ...

    async def create(
        self, collection: Union[Dict[str, Any], Collection], **kwargs
    ) -> Response:
        ...

    async def update(
        self,
        collection_id: str,
        collection: Union[Dict[str, Any], Collection],
        **kwargs,
    ) -> Response:
        ...

    async def delete(self, collection_id: str, **kwargs) -> Response:
        ...

    # Collection-specific methods
    async def get_info(self, collection_id: str, **kwargs) -> Response:
        ...

    async def get_contents(self, collection_id: str, **kwargs) -> Response:
        ...

    async def add_content(
        self, collection_id: str, content_data: Dict[str, Any], **kwargs
    ) -> Response:
        ...

    async def remove_content(
        self, collection_id: str, content_id: str, **kwargs
    ) -> Response:
        ...
