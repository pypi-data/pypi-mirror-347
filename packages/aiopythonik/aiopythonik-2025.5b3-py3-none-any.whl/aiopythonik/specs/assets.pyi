from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional, Union

from pythonik.models.base import Response
from pythonik.specs.assets import Asset

from .._pythonik_patches import AssetSpec
from ..rate_limiting import RateLimitHandler


class AsyncAssetSpec:
    _sync_spec: AssetSpec
    _executor: Optional[ThreadPoolExecutor]
    _rate_limit_handler: Optional[RateLimitHandler]

    def __init__(
        self,
        sync_spec: AssetSpec,
        executor: Optional[Any] = None,
        rate_limit_handler: Optional[Any] = None,
    ) -> None:
        ...

    async def get(self, asset_id: str, **kwargs) -> Response:
        ...

    async def fetch(self, **kwargs) -> Response:
        ...

    async def create(
        self, asset: Union[Dict[str, Any], Asset], **kwargs
    ) -> Response:
        ...

    async def update_asset(
        self, asset_id: str, asset: Union[Dict[str, Any], Asset], **kwargs
    ) -> Response:
        ...

    async def partial_update_asset(
        self, asset_id: str, asset: Union[Dict[str, Any], Asset], **kwargs
    ) -> Response:
        ...

    async def delete(self, asset_id: str, **kwargs) -> Response:
        ...

    async def bulk_delete(self, asset_ids: List[str], **kwargs) -> Response:
        ...

    async def permanently_delete(self, asset_id: str, **kwargs) -> Response:
        ...

    # Version-related methods
    async def create_version(
        self, asset_id: str, version_data: Dict[str, Any], **kwargs
    ) -> Response:
        ...

    async def create_version_from_asset(
        self, asset_id: str, source_asset_id: str, **kwargs
    ) -> Response:
        ...

    async def update_version(
        self,
        asset_id: str,
        version_id: str,
        version_data: Dict[str, Any],
        **kwargs,
    ) -> Response:
        ...

    async def partial_update_version(
        self,
        asset_id: str,
        version_id: str,
        version_data: Dict[str, Any],
        **kwargs,
    ) -> Response:
        ...

    async def delete_version(
        self, asset_id: str, version_id: str, **kwargs
    ) -> Response:
        ...

    async def promote_version(
        self, asset_id: str, version_id: str, **kwargs
    ) -> Response:
        ...

    async def delete_old_versions(self, asset_id: str, **kwargs) -> Response:
        ...

    # Segment-related methods
    async def create_segment(
        self, asset_id: str, segment_data: Dict[str, Any], **kwargs
    ) -> Response:
        ...

    async def update_segment(
        self,
        asset_id: str,
        segment_id: str,
        segment_data: Dict[str, Any],
        **kwargs,
    ) -> Response:
        ...

    async def partial_update_segment(
        self,
        asset_id: str,
        segment_id: str,
        segment_data: Dict[str, Any],
        **kwargs,
    ) -> Response:
        ...

    # History-related methods
    async def fetch_asset_history_entities(
        self, asset_id: str, **kwargs
    ) -> Response:
        ...

    async def create_history_entity(
        self,
        asset_id: str,
        operation_description: str,
        operation_type: str,
        **kwargs,
    ) -> Response:
        ...
