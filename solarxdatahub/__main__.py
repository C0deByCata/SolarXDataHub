"""Main module for the SolarX Data Hub application."""

import logging

from solarxdatahub.core.controller import run

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    run()
    logger.info("Data hub completed")
