"""stdout driver — human-readable or JSONL to console."""
from __future__ import annotations

import json
import sys

from tiktok_views_generator.drivers.base import BaseDriver
from tiktok_views_generator.models.result import ViewResult


class StdoutDriver(BaseDriver):
    name = "stdout"

    def __init__(self, jsonl: bool = False, color: bool = True) -> None:
        self.jsonl = jsonl
        self.color = color

    async def emit(self, result: ViewResult) -> None:
        if self.jsonl:
            sys.stdout.write(json.dumps(result.model_dump()) + "\n")
            sys.stdout.flush()
            return
        mark = "OK " if result.status == "ok" else "ERR"
        sys.stdout.write(f"[{mark}] {result.url} session={result.session_id}\n")
        sys.stdout.flush()