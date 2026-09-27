"""Base ingest handler — yields ViewJob objects from a raw source."""
from __future__ import annotations

import abc
from typing import AsyncIterator

from tiktok_views_generator.models.job import ViewJob


class BaseIngestHandler(abc.ABC):
    """Ingest handlers are stateless. One instance per pipeline run."""

    name: str = "base"

    @abc.abstractmethod
    def ingest(self, source: str) -> AsyncIterator[ViewJob]:
        """Yield ViewJob for each URL found in `source`."""
        raise NotImplementedError