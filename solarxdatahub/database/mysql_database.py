"""Module for MySQL database connection and operations."""

import logging
import os
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
from pymysql.connections import Connection
from pymysql.cursors import DictCursor

logger = logging.getLogger(__name__)


class MySQLDatabase:
    """MySQL database connection and operations."""

    _host: str
    _port: int
    _user: str
    _password: str
    _ssl_key: Optional[str]
    _database: str
    _connection: Optional[Connection]

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        ssl_key: Optional[str],
        database: str,
    ) -> None:
        """Initialize the MySQL database connection."""
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._ssl_key = ssl_key
        self._database = database
        self._connection = None

    def _ensure_connection(self) -> None:
        if self._connection is None:
            raise ConnectionError(
                "You are not connected to the database, please connect first."
            )
        try:
            self._connection.ping(reconnect=True)
            logger.debug("Ping to the database successful")
        except Exception as e:
            logger.exception("Failed to ping the database %s", e)
            raise

    def connect(self) -> None:
        """Connect to the MySQL database."""
        connection_args = {
            "host": self._host,
            "port": self._port,
            "user": self._user,
            "password": self._password,
            "database": self._database,
            "cursorclass": DictCursor,
        }

        # Configuración SSL: se admite None, una ruta válida o una cadena indicador de habilitar SSL sin certificado.
        if self._ssl_key is not None:
            if isinstance(self._ssl_key, dict):
                connection_args["ssl"] = self._ssl_key
            elif isinstance(self._ssl_key, str):
                # Si la cadena corresponde a una ruta de archivo existente, úsala como certificado
                if os.path.exists(self._ssl_key):
                    connection_args["ssl"] = {"ca": self._ssl_key}
                else:
                    # Si no es una ruta válida, asumimos que se quiere habilitar SSL sin certificado.
                    # Por ejemplo, si se pasa "enabled" o "true".
                    connection_args["ssl"] = {}
            else:
                raise ValueError(
                    "Invalid SSL key type, must be a dictionary or a string"
                )

        try:
            self._connection = Connection(**connection_args)
            logger.info("Connected to the MySQL database")
        except Exception as e:
            logger.error("Failed to connect to the MySQL database: %s", e)
            raise

    def disconnect(self) -> None:
        """Disconnect from the MySQL database."""
        if self._connection is None:
            raise ConnectionError(
                "You are not connected to the database, please connect first."
            )

        try:
            self._connection.close()
            self._connection = None
            logger.info("Disconnected from the MySQL database")

        except Exception as e:
            logger.error("Failed to disconnect from the MySQL database: %s", e)
            raise

    def ping(self) -> None:
        """Ping the MySQL database."""
        if self._connection is None:
            raise ConnectionError(
                "You are not connected to the database, please connect first."
            )

        self._connection.ping(reconnect=True)

    def read(
        self,
        query: str,
        params: Optional[Union[Dict[str, Any], list[Any]]] = None,
        as_df: bool = False,
    ) -> Union[List[Dict], pd.DataFrame]:
        """Read data from the MySQL database."""
        self._ensure_connection()
        try:
            with self._connection.cursor() as cursor:
                if params is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, params)
                result = cursor.fetchall()
                logger.debug("Query executed: %s, with params: %s", query, params)
                if as_df:
                    return pd.DataFrame(result)
                return list(result)
        except Exception as e:
            logger.exception("Failed to read from the database: %s", e)
            raise

    def write(
        self,
        query: str,
        data: Union[List[Dict], Tuple, pd.DataFrame],
        commit: bool = True,
    ) -> int:
        """Write data to the MySQL database."""
        self._ensure_connection()

        try:
            with self._connection.cursor() as cursor:
                if isinstance(data, list):
                    cursor.executemany(query, data)
                elif isinstance(data, tuple):
                    cursor.execute(query, data)
                elif isinstance(data, pd.DataFrame):
                    data = data.to_dict(orient="records")
                    cursor.executemany(query, data)
                elif data is None:
                    cursor.execute(query)
                else:
                    raise TypeError("Data type not supported")
                affected_rows = cursor.rowcount
                logger.debug("Query executed: %s, with data: %s", query, data)
            if commit:
                self._connection.commit()
                logger.debug("Transaction committed")
            return affected_rows
        except Exception as e:
            logger.exception("Failed to write to the database: %s", e)
            self._connection.rollback()
            logger.info("Transaction rolled back due to error")
            raise

    def commit(self) -> None:
        """Commit the transaction."""
        self._ensure_connection()
        try:
            self._connection.commit()
            logger.debug("Transaction committed")
        except Exception as e:
            logger.exception("Failed to commit the transaction: %s", e)
            raise

    def begin(self) -> None:
        """Begin a transaction."""
        self._ensure_connection()
        try:
            self._connection.begin()
            logger.debug("Transaction started")
        except Exception as e:
            logger.exception("Failed to start the transaction: %s", e)
            raise

    def rollback(self) -> None:
        """Rollback the transaction."""
        self._ensure_connection()
        try:
            self._connection.rollback()
            logger.debug("Transaction rolled back")
        except Exception as e:
            logger.exception("Failed to roll back the transaction: %s", e)
            raise
