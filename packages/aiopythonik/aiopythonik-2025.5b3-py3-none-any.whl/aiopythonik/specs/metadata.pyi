from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Literal, Optional, Union

from pythonik.models.base import Response

from .._pythonik_patches import MetadataSpec
from .._pythonik_patches.models import (
    CreateViewRequest,
    UpdateViewRequest,
    ViewMetadata,
)
from ..rate_limiting import RateLimitHandler


class AsyncMetadataSpec:
    _sync_spec: MetadataSpec
    _executor: Optional[ThreadPoolExecutor]
    _rate_limit_handler: Optional[RateLimitHandler]

    def __init__(
        self,
        sync_spec: MetadataSpec,
        executor: Optional[Any] = None,
        rate_limit_handler: Optional[Any] = None,
    ) -> None:
        ...

    # Views methods
    async def get_views(self, **kwargs) -> Response:
        ...

    async def get_view(
        self,
        view_id: str,
        merge_fields: Optional[bool] = None,
        **kwargs
    ) -> Response:
        ...

    async def create_view(
        self,
        view: Union[CreateViewRequest, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        ...

    async def update_view(
        self,
        view_id: str,
        view: Union[UpdateViewRequest, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        ...

    async def replace_view(
        self,
        view_id: str,
        view: Union[CreateViewRequest, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        ...

    async def delete_view(self, view_id: str, **kwargs) -> Response:
        ...

    # Metadata methods
    async def get_asset_metadata(
        self,
        asset_id: str,
        view_id: str,
        intercept_404: Union[ViewMetadata, bool] = False,
        **kwargs,
    ) -> Response:
        ...

    async def update_asset_metadata(
        self, asset_id: str, view_id: str, metadata: Dict[str, Any], **kwargs
    ) -> Response:
        ...

    async def get_object_metadata(
        self,
        object_type: Literal["assets", "collections", "segments"],
        object_id: str,
        view_id: str,
        intercept_404: Union[ViewMetadata, bool] = False,
        **kwargs,
    ) -> Response:
        ...

    async def get_object_metadata_direct(
        self,
        object_type: Literal["assets", "collections", "segments"],
        object_id: str,
        intercept_404: Union[ViewMetadata, bool] = False,
        **kwargs,
    ) -> Response:
        ...
