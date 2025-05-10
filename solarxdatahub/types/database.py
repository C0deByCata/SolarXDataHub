"""Data types for working with database"""

from typing import Optional, TypedDict


class DatabaseConnectionConfiguration(TypedDict):
    """Database connection configuration parameters"""

    host: str
    port: int
    user: str
    password: str
    ssl_key: Optional[str]
