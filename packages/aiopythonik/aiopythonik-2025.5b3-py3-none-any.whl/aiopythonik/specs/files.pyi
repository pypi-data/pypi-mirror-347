from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pythonik.models.base import Response
from pythonik.models.files.file import File

from .._pythonik_patches import FilesSpec
from ..rate_limiting import RateLimitHandler


class AsyncFilesSpec:
    _sync_spec: FilesSpec
    _executor: Optional[ThreadPoolExecutor]
    _rate_limit_handler: Optional[RateLimitHandler]

    def __init__(
        self,
        sync_spec: FilesSpec,
        executor: Optional[Any] = None,
        rate_limit_handler: Optional[Any] = None,
    ) -> None:
        ...

    # Storage-related methods
    async def get_storages(self, **kwargs) -> Response:
        ...

    async def get_storage(self, storage_id: str, **kwargs) -> Response:
        ...

    async def update_storage(
        self, storage_id: str, storage_data: Dict[str, Any], **kwargs
    ) -> Response:
        ...

    async def fetch_storage_files(self, storage_id: str, **kwargs) -> Response:
        ...

    async def create_storage_file(
        self,
        storage_id: str,
        body: Union[File, Dict[str, Any]],
        exclude_defaults: bool = True,
        **kwargs,
    ) -> Response:
        ...

    # Asset files methods
    async def get_asset_files(self, asset_id: str, **kwargs) -> Response:
        ...

    async def create_asset_file(
        self, asset_id: str, file_data: Dict[str, Any], **kwargs
    ) -> Response:
        ...

    async def partial_update_asset_file(
        self, asset_id: str, file_id: str, file_data: Dict[str, Any], **kwargs
    ) -> Response:
        ...

    # Asset formats methods
    async def create_asset_format(
        self, asset_id: str, format_data: Dict[str, Any], **kwargs
    ) -> Response:
        ...

    async def fetch_asset_format_components(
        self, asset_id: str, format_id: str, **kwargs
    ) -> Response:
        ...

    # File sets methods
    async def create_asset_file_sets(
        self, asset_id: str, file_sets_data: Dict[str, Any], **kwargs
    ) -> Response:
        ...

    # Deleted objects methods
    async def get_deleted_file_sets(self, **kwargs) -> Response:
        ...

    async def get_deleted_filesets(self, **kwargs) -> Response:
        ...  # Alias

    async def get_deleted_formats(self, **kwargs) -> Response:
        ...

    # Jobs methods
    async def create_mediainfo_job(
        self,
        asset_id: str,
        file_id: str,
        priority: Optional[int] = 5,
        **kwargs
    ) -> Response:
        ...

    async def create_transcode_job(
        self,
        asset_id: str,
        file_id: str,
        priority: Optional[int] = 5,
        **kwargs
    ) -> Response:
        ...

    # Custom methods
    async def get_files_by_checksum(
        self,
        checksum_or_file: Union[str, Path],
        per_page: Optional[int] = None,
        page: Optional[int] = None,
        chunk_size: int = 8192,
        **kwargs,
    ) -> Response:
        ...
