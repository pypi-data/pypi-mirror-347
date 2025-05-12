import logging
import os
from typing import Optional
from rich.logging import RichHandler


def setup_logger(
    name: str = "laoshu",
    level: Optional[str] = None,
) -> logging.Logger:
    if level is None:
        level = os.environ.get("LOG_LEVEL", "INFO").upper()

    numeric_level = getattr(logging, level, logging.INFO)

    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)

    return logger


logger = setup_logger()
