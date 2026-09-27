from tiktok_views_generator.drivers.jsonl_driver import JsonlDriver
from tiktok_views_generator.drivers.sqlite_driver import SqliteDriver
from tiktok_views_generator.drivers.stdout_driver import StdoutDriver

DRIVERS = {
    "stdout": StdoutDriver,
    "jsonl": JsonlDriver,
    "sqlite": SqliteDriver,
}

__all__ = ["DRIVERS"]