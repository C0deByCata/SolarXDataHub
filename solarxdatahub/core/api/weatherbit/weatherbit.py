"""Module to interact with the Weatherbit API."""

from datetime import datetime

import pandas as pd
import requests
from loguru import logger

from solarxdatahub.config import Weatherbit
from solarxdatahub.database.crud import insert_weatherbit_current_
from solarxdatahub.models.model_weatherbit import WeatherbitResponse, WeatherDataResult


class WeatherbitAPI:
    """Class to interact with the Weatherbit API."""

    def __init__(self):
        self.api_url = Weatherbit.WB_BASE_URL
        self.api_key = Weatherbit.WB_API_KEY
        self.latitude = Weatherbit.LATITUDE
        self.longitude = Weatherbit.LONGITUDE
        self.units = Weatherbit.UNITS
        self.language = Weatherbit.LANGUAGE
        self.params = {
            "lat": self.latitude,
            "lon": self.longitude,
            "key": self.api_key,
            "units": self.units,
            "lang": self.language,
        }

    def get_current_weather(self) -> None:
        """Get the current weather from the Weatherbit API."""
        try:
            response = requests.get(self.api_url, params=self.params, timeout=10)
            response.raise_for_status()
            data = response.json()
            weatherbit_response = WeatherbitResponse.from_api(data)
            if not weatherbit_response.success or weatherbit_response.result is None:
                logger.error(
                    "API Weatherbit returned an error: {}",
                    weatherbit_response.exception,
                )
                return None
            return weatherbit_response
        except requests.exceptions.RequestException as e:
            logger.error(
                "An error occurred getting the data from the Weatherbit API: {}", e
            )
            return None

    def process_weatherbit_response(
        self, response: WeatherbitResponse, request_time: datetime
    ) -> None:
        """
        Procesa la respuesta de Weatherbit para preparar los datos a insertar en la BD.

        Extrae el primer registro de datos (result), lo convierte a diccionario,
        añade el campo 'calculation_datetime' (redondeado a la hora) y convierte el
        campo 'sources' en cadena si es necesario. Finalmente, crea un DataFrame,
        lo convierte a lista de diccionarios y llama a la función de inserción.

        Args:
            response (WeatherbitResponse): Respuesta adaptada de Weatherbit.
            request_time (datetime): Momento en que se realizó la petición.
        """
        result: WeatherDataResult = response.result

        df_weather = pd.DataFrame(
            [
                {
                    "calculation_datetime": request_time,
                    "wind_cdir": result.wind_cdir,
                    "rh": result.rh,
                    "pod": result.pod,
                    "lon": result.lon,
                    "pres": result.pres,
                    "timezone": result.timezone,
                    "ob_time": result.ob_time,
                    "country_code": result.country_code,
                    "clouds": result.clouds,
                    "vis": result.vis,
                    "wind_spd": result.wind_spd,
                    "gust": result.gust,
                    "wind_cdir_full": result.wind_cdir_full,
                    "app_temp": result.app_temp,
                    "state_code": result.state_code,
                    "ts": result.ts,
                    "h_angle": result.h_angle,
                    "dewpt": result.dewpt,
                    "weather_icon": result.weather.icon,
                    "weather_description": result.weather.description,
                    "weather_code": result.weather.code,
                    "uv": result.uv,
                    "aqi": result.aqi,
                    "station": result.station,
                    "sources": ",".join(result.sources)
                    if isinstance(result.sources, list)
                    else result.sources,
                    "wind_dir": result.wind_dir,
                    "elev_angle": result.elev_angle,
                    "datetime": result.datetime,
                    "precip": result.precip,
                    "ghi": result.ghi,
                    "dni": result.dni,
                    "dhi": result.dhi,
                    "solar_rad": result.solar_rad,
                    "city_name": result.city_name,
                    "sunrise": result.sunrise,
                    "sunset": result.sunset,
                    "temp": result.temp,
                    "lat": result.lat,
                    "slp": result.slp,
                    "snow": result.snow,
                }
            ]
        )
        insert_weatherbit_current_(df_weather)
        logger.info(
            "Datos meteorológicos insertados/actualizados correctamente en weatherbit_current."
        )
