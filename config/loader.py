"""Config loader — YAML + env overlay. No logic leaks downstream."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

_ENV_MAP = {
    "TTVG_CONCURRENCY": ("runtime", "concurrency", int),
    "TTVG_REQUESTS_PER_SESSION": ("runtime", "requests_per_session", int),
    "TTVG_WATCH_SECONDS": ("runtime", "watch_seconds", int),
    "TTVG_PROXY_FILE": ("proxy", "pool_file", str),
    "TTVG_SESSION_DIR": ("session", "dir", str),
    "TTVG_DRIVER": ("driver", "name", str),
    "TTVG_LOG_LEVEL": ("logging", "level", str),
}


def _set(cfg: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    node = cfg
    for key in path[:-1]:
        node = node.setdefault(key, {})
    node[path[-1]] = value


def load_config(path: str | os.PathLike[str] | None = None) -> dict[str, Any]:
    cfg_path = Path(path or os.getenv("TTVG_CONFIG", "config/default.yaml"))
    with cfg_path.open("r", encoding="utf-8") as fh:
        cfg: dict[str, Any] = yaml.safe_load(fh) or {}

    for env_key, (section, key, caster) in _ENV_MAP.items():
        raw = os.getenv(env_key)
        if raw is None:
            continue
        _set(cfg, (section, key), caster(raw))

    return cfg