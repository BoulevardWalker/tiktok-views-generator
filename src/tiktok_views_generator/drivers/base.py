"""Base output driver."""
from __future__ import annotations

import abc

from tiktok_views_generator.models.result import ViewResult


class BaseDriver(abc.ABC):
    name: str = "base"

    @abc.abstractmethod
    async def emit(self, result: ViewResult) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        return None