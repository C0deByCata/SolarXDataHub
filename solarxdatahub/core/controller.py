"""Methods for controlling the data hub."""

from datetime import datetime, timedelta

import pandas as pd
from loguru import logger

from solarxdatahub.config import Logging, OpenWeather, Weatherbit
from solarxdatahub.core.api.openweather.openweather import OpenWeatherAPI
from solarxdatahub.core.api.solaxcloud.solaxcloud import SolaxCloudAPI
from solarxdatahub.core.api.weatherbit.weatherbit import WeatherbitAPI
from solarxdatahub.database.connection import DataBaseConnection
from solarxdatahub.database.crud import (
    get_master_tb_request_options,
    get_openweather_last_request,
    get_openweather_requests_log,
    get_weatherbit_last_request,
    get_weatherbit_requests_log,
    insert_weatherbit_requests_log_,
)


def prepare_environment():
    """Prepare the environment for the data hub."""
    Logging.configure_logger()
    DataBaseConnection.connect()


def run():
    """Run the data hub."""
    try:
        prepare_environment()
        process_solaxcloud_data(SolaxCloudAPI())
        process_openweather_data(OpenWeatherAPI())
        process_weather_data(WeatherbitAPI())
    except (ValueError, KeyError, ConnectionError) as e:
        logger.exception("A specific error occurred: {}", e)
        raise
    except Exception as e:
        logger.exception("An error occurred: {}", e)
        raise
    finally:
        DataBaseConnection.disconnect()


def process_solaxcloud_data(client: SolaxCloudAPI):
    """Process the data from the Solax Cloud API.

    Args:
        client (SolaxCloudAPI): The Solax Cloud API client.
    """
    api_response = client.get_real_time_data()
    if api_response is None or not api_response.success or api_response.result is None:
        logger.error("No data was received from the Solax Cloud API")
        return
    client.process_solaxcloud_response(api_response)


def ensure_hour_interval_or_skip(
    df_last_exec: pd.DataFrame, interval_minutes: int = 60
) -> bool:
    """
    Verifica si ha pasado al menos `interval_minutes` desde la última ejecución exitosa.

    Args:
        df_last_exec (pd.DataFrame): DataFrame con una columna 'last_request' de tipo datetime.
        interval_minutes (int): Tiempo mínimo que debe haber pasado desde la última ejecución.

    Returns:
        bool: True si puede ejecutarse, False si debe omitirse.
    """
    if df_last_exec.empty or pd.isna(df_last_exec.iloc[0]["last_request"]):
        return True  # No hay registro previo, se puede ejecutar

    last_time = pd.to_datetime(df_last_exec.iloc[0]["last_request"])
    elapsed = datetime.now() - last_time
    return elapsed.total_seconds() >= interval_minutes * 60


def process_weather_data(client: WeatherbitAPI) -> None:
    """
    Controla la lógica para llamar a la API de Weatherbit:
        - Comprueba que no se hayan excedido las {Weatherbit.WB_DAILY_LIMIT} peticiones diarias.
        - Realiza la petición.
        - Registra la petición en weatherbit_requests_log.
        - Si la respuesta es válida, delega el procesamiento a client.process_weatherbit_response.
    """
    # Consulta el número de peticiones realizadas hoy
    req_log_df = get_weatherbit_requests_log()
    total_requests = (
        int(req_log_df.iloc[0]["total_requests"]) if not req_log_df.empty else 0
    )

    if total_requests >= int(Weatherbit.WB_DAILY_LIMIT):
        logger.error(
            f"Se alcanzó el límite de {Weatherbit.WB_DAILY_LIMIT} peticiones diarias para Weatherbit."
        )
        return

    interval_minutes = 60
    weatherbit_last_request = get_weatherbit_last_request()
    if not ensure_hour_interval_or_skip(weatherbit_last_request):
        # Recalcular cuánto tiempo queda
        last_time = pd.to_datetime(weatherbit_last_request.iloc[0]["last_request"])
        elapsed = datetime.now() - last_time
        remaining = timedelta(minutes=interval_minutes) - elapsed
        # Log con tiempo restante
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        logger.warning(
            f"Saltando petición a Weatherbit: "
            f"faltan {mins} min {secs} s para la siguiente petición."
        )
        return

    current_request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    api_response = client.get_current_weather()
    http_status_code = api_response.code if api_response else 0

    log_data = [{"request_datetime": current_request_time, "status": http_status_code}]
    df_log = pd.DataFrame(log_data)
    insert_weatherbit_requests_log_(df_log.to_dict(orient="records"))

    if not api_response or not api_response.success:
        logger.error("No se recibieron datos de la API Weatherbit.")
        return

    # Procesa la respuesta delegando en el método del cliente
    client.process_weatherbit_response(api_response, current_request_time)


def process_openweather_data(client: OpenWeatherAPI) -> None:
    """
    Controla la lógica para llamar a la API de OpenWeather:
        - Comprueba que no se hayan excedido las {OpenWeather.OW_DAILY_LIMIT} peticiones diarias.
        - Realiza la petición.
        - Registra la petición en openweather_requests_log.
        - Si la respuesta es válida, delega el procesamiento a client.process_openweather_response.
    """
    # Consulta el número de peticiones realizadas hoy
    req_log_df = get_openweather_requests_log()
    request_options = get_master_tb_request_options()
    if request_options.empty:
        logger.error("No se encontraron opciones de solicitud para OpenWeather.")
        return

    total_requests = (
        int(req_log_df.iloc[0]["total_requests"]) if not req_log_df.empty else 0
    )

    if total_requests >= int(OpenWeather.OW_DAILY_LIMIT):
        logger.error(
            f"Se alcanzó el límite de {OpenWeather.OW_DAILY_LIMIT} peticiones diarias para OpenWeather."
        )
        return

    interval_minutes = 60
    openweather_last_request = get_openweather_last_request()
    if not ensure_hour_interval_or_skip(openweather_last_request):
        # Recalcular cuánto tiempo queda
        last_time = pd.to_datetime(openweather_last_request.iloc[0]["last_request"])
        elapsed = datetime.now() - last_time
        remaining = timedelta(minutes=interval_minutes) - elapsed
        # Log con tiempo restante
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        logger.warning(
            f"Saltando petición a OpenWeather: "
            f"faltan {mins} min {secs} s para la siguiente petición."
        )
        return

    current_weather = client.get_current_weather(request_options)
    air_pollution = client.get_air_pollution(request_options)

    if not current_weather or not current_weather.success:
        logger.error("No se recibieron datos de la API OpenWeather.")
    else:
        client.process_openweather_response_current(current_weather)

    if not air_pollution or not air_pollution.success:
        logger.error("No se recibieron datos de la API OpenWeather.")
    else:
        client.process_openweather_air_pollution_response(air_pollution)

    logger.info("Successfully processed all data from the OpenWeather API.")
