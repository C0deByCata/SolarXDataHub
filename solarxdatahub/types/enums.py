"""Module for defining enums used in the SolarX Data Hub."""

from enum import Enum


class WorkEnvironment(Enum):
    """Enumeration of work environments."""

    DEVELOPMENT = "development"  # read from production and insert into local
    PRODUCTION = "production"  # read and insert into production
