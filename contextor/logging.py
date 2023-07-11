from typing import Final
from types import TracebackType
from datetime import datetime
from pathlib import Path
import sys
import logging

from loguru import logger

from .config import config


LOGS_PATH: Final[Path] = Path.cwd() / "logs"
LOGS_PATH.mkdir(exist_ok=True)

current_time = datetime.utcnow().strftime("%d.%m.%y_%H.%M.%S.%f")
filename = f"log_{current_time}.txt"
FORMAT: Final[str] = (
    "<green>{time:DD.MM.YY HH:MM:ss!UTC}</green> "
    "[<level>{level}</level>] ({name}) {message}"
)

stream_handler_config = {
    "sink": sys.stdout,
    "level": "INFO",
    "format": FORMAT,
}
main_handler_config = {
    "sink": LOGS_PATH / filename,
    "level": "INFO",
    "format": FORMAT,
    "retention": config.logging.history_length,
}
debug_handler_config = {
    "sink": LOGS_PATH / f"debug_{filename}",
    "level": "DEBUG",
    "format": FORMAT,
    "retention": config.logging.history_length,
}

handlers_configs = [stream_handler_config, main_handler_config]
if config.logging.debug_files:
    handlers_configs.append(debug_handler_config)

config = {
    "handlers": handlers_configs,
}
handlers = logger.configure(**config)


def _handle_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType
) -> None:
    exc_info = (exc_type, exc_value, exc_traceback)
    if not issubclass(exc_type, KeyboardInterrupt):
        error_logger.opt(exception=exc_info).error("Uncaught exception")
    return sys.__excepthook__(exc_type, exc_value, exc_traceback)


class InterceptHandler(logging.Handler):
    """ From logging to loguru """

    def emit(self, record):
        # Get corresponding Loguru level if it exists.
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        depth = 6
        frame = sys._getframe(depth)
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
    datefmt="%d.%m.%y %H:%M:%S",
    handlers=(InterceptHandler(), ),
    level=0,
    force=True
)

error_logger = logger.bind(name="errors")  # FIXME: doesn't changes {name} in format
sys.excepthook = _handle_exception
