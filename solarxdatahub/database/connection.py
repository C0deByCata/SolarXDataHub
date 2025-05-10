"""Module to define the connection to the database."""

import functools
import re
from typing import Callable

import pandas as pd
from loguru import logger

from solarxdatahub.config import Database
from solarxdatahub.database.mysql_database import MySQLDatabase


def db_error_handler(func: Callable) -> Callable:
    """Decorator to handle database errors.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The decorated function.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception("An error occurred: {}", e)
            raise

    return wrapper


class DataBaseConnection:
    """Class to define the work with the database."""

    __connections: dict[str, MySQLDatabase] = {}

    @classmethod
    @db_error_handler
    def connect(cls, host_name: str | None = None) -> None:
        """Connect to the database.

        Args:
            host_name (str | None, optional): _description_. Defaults to None.

        Raises:
            ValueError: host_name is not in the configuration.
        """
        host_names = Database.host_names()
        names = [host_name] if host_name else host_names

        for name in names:
            if name not in host_names:
                raise ValueError(f"host_name {name} is not in the configuration.")
            if name not in cls.__connections:
                database = MySQLDatabase(**Database[name].value)
                database.connect()
                cls.__connections[name] = database
                logger.debug("Connected to database {}.", name)

    @classmethod
    @db_error_handler
    def disconnect(cls, host_name: str | None = None) -> None:
        """Disconnect from the database.

        Args:
            host_name (str | None, optional): _description_. Defaults to None.
        """
        if host_name:
            if host_name not in cls.__connections:
                raise ConnectionError(f"No connection found for the host: {host_name}")
            cls.__connections[host_name].disconnect()
            del cls.__connections[host_name]
            logger.info("Disconnected from database {}.", host_name)
        else:
            # Disconnect from all databases and clean the dictionary
            for connection in list(cls.__connections.values()):
                connection.disconnect()
            cls.__connections.clear()
            logger.info("Disconnected from all databases.")

    @classmethod
    @db_error_handler
    def read(
        cls, host_name: str, query: Callable, params: dict = {}, as_df: bool = False
    ) -> list[dict] | pd.DataFrame:
        """Read data from the database.

        Args:
            host_name (str): The name of the host to read from.
            query (Callable): The query to execute.
            params (dict): The parameters to pass to the query.
            as_df (bool, optional): Return the data as a DataFrame. Defaults to False.

        Returns:
            list[dict] | pd.DataFrame: The data read from the database.
        """
        if host_name not in cls.__connections:
            raise ConnectionError(
                "You are not connected to the database, please connect first."
            )
        logger.debug(
            "Reading data from {}", re.search(r"read_(.*)", query.__name__).group(1)
        )
        return cls.__connections[host_name].read(query=query(**params), as_df=as_df)

    @classmethod
    @db_error_handler
    def write(
        cls,
        host_name: str,
        query: Callable,
        data: list[dict] | pd.DataFrame,
        commit: bool = True,
    ) -> int:
        """Write data to the database.

        Args:
            host_name (str): The name of the host to write to.
            query (Callable): The query to execute.
            data (list[dict] | pd.DataFrame): The data to write.
            commit (bool, optional): Commit the transaction. Defaults to True.

        Returns:
            int: The number of rows affected.
        """
        if host_name not in cls.__connections:
            raise ConnectionError(
                "You are not connected to the database, please connect first."
            )

        inserted_rows = cls.__connections[host_name].write(
            query=query(), data=data, commit=commit
        )

        updated_rows = len(data) - inserted_rows
        table_name_match = re.search(r"insert_(.*)", query.__name__)
        table_name = table_name_match.group(1) if table_name_match else "unknown table"

        logger.info(
            "Host: {}, {} data inserted and {} data updated in {}.",
            host_name,
            inserted_rows,
            updated_rows,
            table_name,
        )
        return inserted_rows

    @classmethod
    @db_error_handler
    def truncate(cls, host_name: str, query: Callable, commit: bool = True) -> None:
        """
        Truncate the table in the database.

        Args:
            host_name (str): The name of the host to truncate.
            query (Callable): A callable que devuelve la cadena SQL.
            commit (bool, optional): Commit the transaction. Defaults to True.
        """
        if host_name not in cls.__connections:
            raise ConnectionError(
                "You are not connected to the database, please connect first."
            )

        cls.__connections[host_name].write(query=query(), data=None, commit=commit)

        table_name_match = re.search(r"truncate_(.*)", query.__name__)
        table_name = table_name_match.group(1) if table_name_match else "unknown table"

        logger.info("Host: {}, Table {} truncated.", host_name, table_name)

    @classmethod
    @db_error_handler
    def begin(cls, host_name: str) -> None:
        """
        Begin a transaction.

        Args:
            host_name (str): The name of the host to begin the transaction.
        """
        if host_name not in cls.__connections:
            raise ConnectionError(
                "You are not connected to the database, please connect first."
            )
        cls.__connections[host_name].begin()
        logger.info("Transaction started on host: {}.", host_name)

    @classmethod
    @db_error_handler
    def commit(cls, host_name: str) -> None:
        """
        Commit a transaction.

        Args:
            host_name (str): The name of the host to commit the transaction.
        """
        if host_name not in cls.__connections:
            raise ConnectionError(
                "You are not connected to the database, please connect first."
            )
        cls.__connections[host_name].commit()
        logger.info("Transaction committed on host: {}.", host_name)

    @classmethod
    @db_error_handler
    def rollback(cls, host_name: str) -> None:
        """
        Rollback a transaction.

        Args:
            host_name (str): The name of the host to rollback the transaction.
        """
        if host_name not in cls.__connections:
            raise ConnectionError(
                "You are not connected to the database, please connect first."
            )
        cls.__connections[host_name].rollback()
        logger.info("Transaction rolled back on host: {}.", host_name)
