"""Module for interacting with the OpenWeather API."""

from datetime import datetime

import pandas as pd
import requests
from loguru import logger

from solarxdatahub.config import OpenWeather
from solarxdatahub.database.crud import (
    insert_openweather_air_pollution_,
    insert_openweather_current_,
    insert_openweather_requests_log_,
)
from solarxdatahub.models.model_openweather import (
    OpenWeatherAirPollutionResponse,
    OpenWeatherCurrentResponse,
)


class OpenWeatherAPI:
    """Clase para interactuar con las APIs de OpenWeather (clima actual y contaminación)."""

    def __init__(self):
        self.lat = OpenWeather.OW_LAT
        self.lon = OpenWeather.OW_LON
        self.api_key = OpenWeather.OW_API_KEY
        self.metrics = OpenWeather.OW_METRICS
        self.lang = OpenWeather.OW_LANG
        self.current_url = OpenWeather.OW_CURRENT_URL
        self.forecast_url = OpenWeather.OW_FORECAST_URL
        self.air_pollution_url = OpenWeather.OW_AIR_POLLUTION_URL
        self.daily_limit = OpenWeather.OW_DAILY_LIMIT

    def get_current_weather(
        self, df_request_options: pd.DataFrame
    ) -> OpenWeatherCurrentResponse:
        """
        Fetches current weather data from the OpenWeather API.

        Returns:
            OpenWeatherCurrentResponse: The current weather data.
        """
        http_status_code = 0
        current_request_time = datetime.now()
        request_option_id = int(
            df_request_options.loc[
                df_request_options["request_type"] == "weather", "id"
            ].iloc[0]
        )

        try:
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "appid": self.api_key,
                "units": self.metrics,
                "lang": self.lang,
            }
            response = requests.get(self.current_url, params=params, timeout=10)
            response.raise_for_status()
            http_status_code = response.status_code
            data = response.json()
            current_weather = OpenWeatherCurrentResponse.from_api(data)
            if not current_weather.success or current_weather.result is None:
                logger.error(
                    "API OpenWeather returned an error: {}", current_weather.exception
                )
        except requests.exceptions.RequestException as e:
            http_status_code = e.response.status_code if e.response is not None else 0
            current_weather = OpenWeatherCurrentResponse(
                success=False,
                result=None,
                exception=str(e),
                code=http_status_code,
            )
            logger.error(
                "An error occurred getting the data from the OpenWeather API: {}", e
            )

        df_log_data = pd.DataFrame(
            [
                {
                    "request_datetime": current_request_time,
                    "request_option_id": request_option_id,
                    "status": http_status_code,
                }
            ]
        )
        insert_openweather_requests_log_(df_log_data)
        return current_weather

    def get_air_pollution(
        self, df_request_options: pd.DataFrame
    ) -> OpenWeatherAirPollutionResponse:
        """
        Fetches air pollution data from the OpenWeather API.

        Returns:
            OpenWeatherAirPollutionResponse: _description_
        """
        current_request_time = datetime.now()
        http_status_code = 0
        request_option_id = int(
            df_request_options.loc[
                df_request_options["request_type"] == "air_pollution", "id"
            ].iloc[0]
        )
        try:
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "appid": self.api_key,
            }
            response = requests.get(self.air_pollution_url, params=params, timeout=10)
            response.raise_for_status()
            http_status_code = response.status_code
            data = response.json()
            air_pollution = OpenWeatherAirPollutionResponse.from_api(data)
            if not air_pollution.success or air_pollution.result is None:
                logger.error(
                    "API OpenWeather returned an error: {}", air_pollution.exception
                )
        except requests.exceptions.RequestException as e:
            http_status_code = e.response.status_code if e.response is not None else 0
            air_pollution = OpenWeatherAirPollutionResponse(
                success=False,
                result=[],
                exception=str(e),
                code=http_status_code,
            )
            logger.error(
                "An error occurred getting the air pollution data from the OpenWeather API: {}",
                e,
            )

        df_log_data = pd.DataFrame(
            [
                {
                    "request_datetime": current_request_time,
                    "request_option_id": request_option_id,
                    "status": http_status_code,
                }
            ]
        )
        insert_openweather_requests_log_(df_log_data)
        return air_pollution

    def process_openweather_response_current(
        self, response: OpenWeatherCurrentResponse
    ):
        """
        Processes the OpenWeather current weather response to prepare the data to insert in the DB.

        Extracts the first data record (result), converts it to a dictionary, adds the 'calculation_datetime'
        field (rounded to the hour) and converts the 'sources' field to a string if necessary. Finally, it
        creates a DataFrame, inserts the data into the DB and logs the operation.

        Args:
            response (OpenWeatherCurrentResponse): The current weather response.
            request_time (datetime): The time the request was made.
        """
        request_time = datetime.now()
        result: OpenWeatherCurrentResponse = response.result
        if response.result is None:
            logger.error(
                "Failed to process current weather response: No valid response received."
            )
            return

        df_current = pd.DataFrame(
            [
                {
                    "calculation_datetime": request_time,
                    "city_name": result.name,
                    "country": result.sys.country,
                    "lat": result.coord.lat,
                    "lon": result.coord.lon,
                    "temp": result.main.temp,
                    "feels_like": result.main.feels_like,
                    "temp_min": result.main.temp_min,
                    "temp_max": result.main.temp_max,
                    "pressure": result.main.pressure,
                    "humidity": result.main.humidity,
                    "sea_level": result.main.sea_level,
                    "grnd_level": result.main.grnd_level,
                    "visibility": result.visibility,
                    "wind_speed": result.wind.speed,
                    "wind_deg": result.wind.deg,
                    "wind_gust": result.wind.gust,
                    "clouds": result.clouds.all,
                    "dt": result.dt,
                    "sunrise": result.sys.sunrise,
                    "sunset": result.sys.sunset,
                    # Si la lista de weather puede tener más de un elemento, se puede almacenar como lista o iterar:
                    "weather_main": [w.main for w in result.weather],
                    "weather_description": [w.description for w in result.weather],
                    "weather_icon": [w.icon for w in result.weather],
                    "timezone": result.timezone,
                    "base": result.base,
                    "city_id": result.id,
                    "sys_type": result.sys.type,
                    "sys_id": result.sys.id,
                    # Para el campo rain, que puede ser None:
                    "rain_1h": result.rain.one_h if result.rain is not None else None,
                    "rain_3h": result.rain.three_h if result.rain is not None else None,
                }
            ]
        )
        insert_openweather_current_(df_current)
        logger.info("Current weather data processed successfully.")

    def process_openweather_air_pollution_response(
        self, response: OpenWeatherAirPollutionResponse
    ):
        """

        Args:
            response (OpenWeatherAirPollutionResponse): _description_
        """
        request_time = datetime.now()
        try:
            lat = self.lat
            lon = self.lon
        except Exception as e:
            logger.warning(
                "No se encontraron coordenadas en la respuesta de contaminación del aire: {}",
                e,
            )
            lat, lon = None, None

        # Verificamos que exista al menos un elemento en la lista de resultados
        if not response.result or len(response.result) == 0:
            logger.error("La respuesta de contaminación del aire no contiene datos.")
            return

        rows = []
        for item in response.result:
            row = {
                "calculation_datetime": request_time,
                "lat": lat,
                "lon": lon,
                "dt": item.dt,
                "aqi": item.main.aqi,
                "co": item.components.co,
                "no": item.components.no,
                "no2": item.components.no2,
                "o3": item.components.o3,
                "so2": item.components.so2,
                "pm2_5": item.components.pm2_5,
                "pm10": item.components.pm10,
                "nh3": item.components.nh3,
            }
            rows.append(row)

        df_air = pd.DataFrame(rows)
        insert_openweather_air_pollution_(df_air)
        logger.info("Air pollution data processed successfully.")
