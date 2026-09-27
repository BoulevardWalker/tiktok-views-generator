"""Base processor — one transformation step over a ViewJob."""
from __future__ import annotations

import abc
from typing import Any

from tiktok_views_generator.models.job import ViewJob


class BaseProcessor(abc.ABC):
    name: str = "base"

    @abc.abstractmethod
    async def run(self, job: ViewJob, ctx: Any) -> ViewJob:
        """Return a (possibly mutated) ViewJob."""
        raise NotImplementedError