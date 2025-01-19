"""Aplicaction configuration"""

import logging
import os


class Logging:
    """Logging configuration"""

    LEVEL = getattr(
        logging, os.getenv("LOGGING_LEVEL", default="").upper(), logging.INFO
    )
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
    DATEFMT = "%Y-%m-%d %H:%M:%S"
    DATEFMT = "%Y-%m-%d %H:%M:%S"
