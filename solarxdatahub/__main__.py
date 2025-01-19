"""Main module for the SolarX Data Hub application."""

import logging

from solarxdatahub.config import Logging

logger = logging.getLogger(__name__)


def prepare_environment():
    """Prepare the environment for the process.

    Raises:
        ControlledException: If the ID of a product is not found.
    """
    logging.basicConfig(
        level=Logging.LEVEL,
        format=Logging.FORMAT,
        datefmt=Logging.DATEFMT,
    )
    logger.info("Environment prepared")


if __name__ == "__main__":
    prepare_environment()
    logger.info("Application started")
