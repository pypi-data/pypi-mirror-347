from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional

from pythonik.models.base import Response

from .._pythonik_patches import JobSpec
from ..rate_limiting import RateLimitHandler


class AsyncJobSpec:
    _sync_spec: JobSpec
    _executor: Optional[ThreadPoolExecutor]
    _rate_limit_handler: Optional[RateLimitHandler]

    def __init__(
        self,
        sync_spec: JobSpec,
        executor: Optional[Any] = None,
        rate_limit_handler: Optional[Any] = None,
    ) -> None:
        ...

    async def get(self, job_id: str, **kwargs) -> Response:
        ...

    async def cancel(self, job_id: str, **kwargs) -> Response:
        ...
