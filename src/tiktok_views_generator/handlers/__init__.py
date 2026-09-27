from tiktok_views_generator.handlers.cli_handler import CliHandler
from tiktok_views_generator.handlers.csv_handler import CsvHandler
from tiktok_views_generator.handlers.paste_handler import PasteHandler

HANDLERS = {
    "cli": CliHandler,
    "csv": CsvHandler,
    "paste": PasteHandler,
}

__all__ = ["HANDLERS"]