"""Aplicaction configuration"""

import os
import sys
from enum import Enum

from loguru import logger

from solarxdatahub.types.database import DatabaseConnectionConfiguration
from solarxdatahub.types.enums import WorkEnvironment

WORK_ENVIRONMENT = getattr(
    WorkEnvironment,
    os.getenv("WORK_ENVIRONMENT", "development").upper(),
    WorkEnvironment.DEVELOPMENT,  # Default value
)


class Logging:
    """
    Configuración de logging usando Loguru.

    Permite elegir entre dos estilos de formateo:
      - "DEFAULT": Solo el nivel se muestra en color (usando etiquetas <level>).
      - "FULL": Toda la línea se muestra en un color que depende del nivel.

    Además, se borra (retiene) automáticamente el archivo de logs según los días definidos
    en la variable de entorno LOG_RETENTION_DAYS.
    """

    # Variables de entorno con valores por defecto.
    LOG_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()
    LOG_FILE = os.getenv("LOG_FILE", "app.log")
    LOG_FORMAT_STYLE = os.getenv("LOG_FORMAT_STYLE", "DEFAULT").upper()
    LOG_RETENTION_DAYS = os.getenv("LOG_RETENTION_DAYS", "7")

    # Formato por defecto: solo el nivel aparece coloreado (usando la etiqueta <level>)
    DEFAULT_LOG_FORMAT = (
        "{time:YYYY-MM-DD HH:mm:ss} | <level>{level}</level> | "
        "{name}:{function}:{line} | {message}"
    )

    @staticmethod
    def _full_color_format(record):
        """
        Función de formateo personalizada para que toda la línea aparezca en color,
        dependiendo del nivel del log.
        """
        # Mapeo de niveles a colores
        color_map = {
            "DEBUG": "blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "magenta",
        }
        level_name = record["level"].name
        color = color_map.get(level_name, "white")
        return (
            f"<{color}>{record['time']:YYYY-MM-DD HH:mm:ss} | "
            f"{record['level'].name} | "
            f"{record['name']}:{record['function']}:{record['line']} | "
            f"{record['message']}</{color}>"
            "\n"
        )

    @staticmethod
    def configure_logger():
        """
        Configura Loguru como sistema de logging:
            - Elimina handlers previos.
            - Configura la salida en consola (con colores) y en archivo.
            - Se aplica la política de retención (borrado automático de logs antiguos) según la variable LOG_RETENTION_DAYS.
            - Se selecciona el formato en función de la variable LOG_FORMAT_STYLE.
        """
        # Remover cualquier handler previo para evitar duplicados.
        logger.remove()

        # Seleccionar el formato según la variable de entorno.
        if Logging.LOG_FORMAT_STYLE == "FULL":
            format_to_use = Logging._full_color_format
        else:
            format_to_use = Logging.DEFAULT_LOG_FORMAT

        # Configurar salida en consola con colores.
        logger.add(
            sys.stdout,
            format=format_to_use,
            level=Logging.LOG_LEVEL,
            colorize=True,  # Asegura que se interpreten las etiquetas de color.
            backtrace=False,  # Muestra backtrace detallado en errores.
            diagnose=True,  # Información adicional en excepciones.
        )

        # Configurar salida en archivo con retención automática.
        retention_str = f"{Logging.LOG_RETENTION_DAYS} days"
        logger.add(
            Logging.LOG_FILE,
            rotation="00:00",  # Rota el archivo a medianoche.
            format=format_to_use,
            level=Logging.LOG_LEVEL,
            retention=retention_str,
        )


class Database(Enum):
    """Configuration of the database connections"""

    TARGET_HOST = DatabaseConnectionConfiguration(
        host=(
            os.getenv("AZURE_PROD_DB_HOST", default="localhost")
            if WORK_ENVIRONMENT == WorkEnvironment.PRODUCTION
            else "localhost"  # development and local environment
        ),
        port=int(os.getenv("DB_PORT", default="3306")),
        user=(
            os.getenv("DB_USER", default="root")
            if WORK_ENVIRONMENT == WorkEnvironment.PRODUCTION
            else "root"  # development and local environment
        ),
        password=(
            os.getenv("DB_PASSWORD", default="docker")
            if WORK_ENVIRONMENT == WorkEnvironment.PRODUCTION
            else "docker"  # development and local environment
        ),
        ssl_key=os.getenv("DB_SSLKEY", default="random"),
        database=os.getenv("DB_DATABASE"),
    )
    SOURCE_HOST = DatabaseConnectionConfiguration(
        host=(
            os.getenv("AZURE_REP_DB_HOST", default="localhost")
            if WORK_ENVIRONMENT
            in [WorkEnvironment.PRODUCTION, WorkEnvironment.DEVELOPMENT]
            else "localhost"  # local environment
        ),
        port=int(os.getenv("DB_PORT", default="3306")),
        user=(
            os.getenv("DB_USER", default="root")
            if WORK_ENVIRONMENT
            in [WorkEnvironment.PRODUCTION, WorkEnvironment.DEVELOPMENT]
            else "root"  # local environment
        ),
        password=(
            os.getenv("DB_PASSWORD", default="docker")
            if WORK_ENVIRONMENT
            in [WorkEnvironment.PRODUCTION, WorkEnvironment.DEVELOPMENT]
            else "docker"  # local environment
        ),
        ssl_key=os.getenv("DB_SSLKEY", default="random"),
        database=os.getenv("DB_DATABASE"),
    )

    @classmethod
    def host_names(cls) -> list[str]:
        """Get the host names"""
        return [element.name for element in cls]


class SolaxCloud:
    """Configuration of the Solax Cloud API"""

    TOKEN_ID = os.getenv("TOKEN_ID")
    WIFI_SN = os.getenv("WIFI_SN")
    API_URL = os.getenv("API_URL")


class Weatherbit:
    """Configuration of the Weatherbit API"""

    WB_API_KEY = os.getenv("WB_API_KEY")
    WB_BASE_URL = os.getenv("WB_BASE_URL")
    LATITUDE = os.getenv("LATITUDE")
    LONGITUDE = os.getenv("LONGITUDE")
    UNITS = os.getenv(
        "UNITS", default="M"
    )  # Unidades de medida (M = Métrico, I = Imperial, S = Científico)
    LANGUAGE = os.getenv("LANGUAGE", default="es")
    WB_DAILY_LIMIT = os.getenv("WB_DAILY_LIMIT", default="50")


class OpenWeather:
    """Configuration of the OpenWeather API"""

    OW_LAT = os.getenv("OW_LAT")
    OW_LON = os.getenv("OW_LON")
    OW_API_KEY = os.getenv("OW_API_KEY")
    OW_METRICS = os.getenv("OW_METRICS", default="metric")
    OW_LANG = os.getenv("OW_LANG", default="es")
    OW_CURRENT_URL = os.getenv("OW_CURRENT_URL")
    OW_FORECAST_URL = os.getenv("OW_FORECAST_URL")
    OW_AIR_POLLUTION_URL = os.getenv("OW_AIR_POLLUTION_URL")
    OW_DAILY_LIMIT = os.getenv("OW_DAILY_LIMIT", default="1000")


class Ntfy:
    """Configuration of the Ntfy API"""

    NTFY_TOPIC = os.getenv("NTFY_TOPIC")
    NTFY_SERVER = os.getenv("NTFY_SERVER")
    NTFY_USER = os.getenv("NTFY_USER")
    NTFY_PASS = os.getenv("NTFY_PASS")
    # Tiempo en minutos para re-notificar
    NTFY_NOTIFY_REPEAT_MINUTES = os.getenv("NTFY_NOTIFY_REPEAT_MINUTES", default="30")
    # Margen de exceso para notificaciones
    NTFY_EXCESS_MARGIN = os.getenv("NTFY_EXCESS_MARGIN", default="50")
