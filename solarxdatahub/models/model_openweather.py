"""File containing the OpenWeatherMap API model."""

# models_openweather.py
from typing import List, Optional

from pydantic import BaseModel, Field


# Modelos comunes
class Coord(BaseModel):
    """Modelo para las coordenadas geográficas

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    lon: float = Field(..., description="Longitud")
    lat: float = Field(..., description="Latitud")


class WeatherDescription(BaseModel):
    """Modelo para la descripción del clima

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    id: int = Field(..., description="ID interno del clima")
    main: str = Field(..., description="Grupo del clima (Rain, Snow, etc.)")
    description: str = Field(..., description="Descripción del clima")
    icon: str = Field(..., description="Código del icono del clima")


class MainWeather(BaseModel):
    """Modelo para las condiciones climáticas principales

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    temp: float = Field(..., description="Temperatura actual (°C)")
    feels_like: float = Field(..., description="Sensación térmica (°C)")
    temp_min: float = Field(..., description="Temperatura mínima (°C)")
    temp_max: float = Field(..., description="Temperatura máxima (°C)")
    pressure: int = Field(..., description="Presión atmosférica (hPa)")
    humidity: int = Field(..., description="Humedad (%)")
    sea_level: Optional[int] = Field(None, description="Presión a nivel del mar (hPa)")
    grnd_level: Optional[int] = Field(None, description="Presión en el suelo (hPa)")


class Wind(BaseModel):
    """Modelo para el viento

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    speed: float = Field(..., description="Velocidad del viento (m/s)")
    deg: int = Field(..., description="Dirección del viento (grados)")
    gust: Optional[float] = Field(None, description="Ráfagas del viento (m/s)")


class Clouds(BaseModel):
    """Modelo para la nubosidad

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    all: int = Field(..., description="Porcentaje de nubosidad")


class Sys(BaseModel):
    """Información adicional del sistema

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    type: Optional[int] = Field(None, description="Tipo interno")
    id: Optional[int] = Field(None, description="ID interno")
    country: str = Field(..., description="Código del país")
    sunrise: int = Field(..., description="Hora de salida del sol (timestamp)")
    sunset: int = Field(..., description="Hora de puesta del sol (timestamp)")


class Rain(BaseModel):
    """Volumen de lluvia en las últimas 1, 3 horas

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    one_h: Optional[float] = Field(
        None, alias="1h", description="Volumen de lluvia en la última hora"
    )
    three_h: Optional[float] = Field(
        None, alias="3h", description="Volumen de lluvia en las últimas 3 horas"
    )


# Modelo para el clima actual
class OpenWeatherCurrentResult(BaseModel):
    """Modelo para el resultado del clima actual de OpenWeatherMap.

    Args:
        BaseModel (pydantic.BaseModel): Base model para Pydantic.
    """

    coord: Coord
    weather: List[WeatherDescription] = Field(
        ..., description="Lista de condiciones climáticas"
    )
    base: str = Field(..., description="Base de la medición")
    main: MainWeather
    visibility: Optional[int] = Field(None, description="Visibilidad en metros")
    wind: Optional[Wind] = None
    rain: Optional[Rain] = None
    clouds: Optional[Clouds] = None
    dt: int = Field(..., description="Hora de la medición (timestamp)")
    sys: Sys
    timezone: int = Field(..., description="Desfase horario (segundos)")
    id: int = Field(..., description="ID interno de la ciudad")
    name: str = Field(..., description="Nombre de la ciudad")
    cod: int = Field(..., description="Código de respuesta")


class OpenWeatherCurrentResponse(BaseModel):
    """Model for the OpenWeatherMap API current weather response.

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.

    Returns:
        OpenWeatherCurrentResponse: Model for the OpenWeatherMap API current weather response.
    """

    success: bool = Field(..., description="True si la respuesta es exitosa")
    result: Optional[OpenWeatherCurrentResult] = Field(
        None, description="Datos del clima actual"
    )
    exception: str = Field("", description="Mensaje de error, si lo hay")
    code: int = Field(0, description="Código de respuesta HTTP")

    @classmethod
    def from_api(cls, data: dict) -> "OpenWeatherCurrentResponse":
        """Crea una instancia de OpenWeatherCurrentResponse a partir de los datos de la API.

        Args:
            data (dict): Datos de la API.

        Returns:
            OpenWeatherCurrentResponse: Modelo para la respuesta del clima actual de OpenWeatherMap.
        """
        # La API devuelve "cod" como número o cadena (p. ej. "200")
        try:
            cod = int(data.get("cod", 0))
        except Exception:
            cod = 0
        if cod == 200:
            result = OpenWeatherCurrentResult(**data)
            return cls(success=True, result=result, code=cod)
        else:
            return cls(
                success=False,
                result=None,
                exception=data.get("message", "Error"),
                code=cod,
            )


# Modelos para el pronóstico (Forecast 5 Day / 3 Hour)
class ForecastCity(BaseModel):
    """Modelo para la ciudad en la respuesta del pronóstico.
    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    id: int = Field(..., description="ID interno de la ciudad")
    name: str = Field(..., description="Nombre de la ciudad")
    coord: Coord
    country: str = Field(..., description="Código del país")
    timezone: int = Field(..., description="Desfase horario (segundos)")
    sunrise: int = Field(..., description="Hora de salida del sol (timestamp)")
    sunset: int = Field(..., description="Hora de puesta del sol (timestamp)")


class ForecastItem(BaseModel):
    """Modelo para un ítem en la lista de pronósticos.

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    dt: int = Field(..., description="Fecha y hora de la predicción (timestamp)")
    main: MainWeather
    weather: List[WeatherDescription] = Field(..., description="Condiciones climáticas")
    clouds: Clouds
    wind: Wind
    visibility: Optional[int] = Field(None, description="Visibilidad (m)")
    pop: float = Field(..., description="Probabilidad de precipitación")
    sys: dict = Field(..., description="Información adicional (por ejemplo, 'pod')")
    dt_txt: str = Field(
        ..., description="Fecha y hora en formato texto (YYYY-MM-DD HH:MM:SS)"
    )


class OpenWeatherForecastResponse(BaseModel):
    """Modelo para la respuesta del pronóstico de OpenWeatherMap.

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.

    Returns:
        OpenWeatherForecastResponse: Modelo para la respuesta del pronóstico de OpenWeatherMap.
    """

    success: bool = Field(..., description="True si la respuesta es exitosa")
    result: List[ForecastItem] = Field(..., description="Lista de predicciones")
    city: ForecastCity = Field(..., description="Información de la ciudad")
    exception: str = Field("", description="Mensaje de error")
    code: int = Field(0, description="Código de respuesta HTTP")

    @classmethod
    def from_api(cls, data: dict) -> "OpenWeatherForecastResponse":
        """
        Método de clase para crear una instancia de OpenWeatherForecastResponse a partir
        de los datos de la API.

        Args:
            data (dict): Datos de la API.
        Returns:
            OpenWeatherForecastResponse: Modelo para la respuesta del pronóstico de OpenWeatherMap.
        """
        if data.get("cod") == "200":
            items = [ForecastItem(**item) for item in data.get("list", [])]
            city = ForecastCity(**data.get("city", {}))
            return cls(success=True, result=items, city=city, code=200)
        else:
            return cls(
                success=False,
                result=[],
                city=None,
                exception=data.get("message", "Error"),
                code=int(data.get("cod", 0)),
            )


# Modelos para la contaminación del aire
class AirPollutionMain(BaseModel):
    """Modelo principal para la contaminación del aire.

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    aqi: int = Field(..., description="Índice de calidad del aire")


class AirPollutionComponents(BaseModel):
    """Modelo para los componentes de la contaminación del aire.

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    co: float = Field(..., description="Monóxido de carbono (µg/m3)")
    no: float = Field(..., description="Óxidos de nitrógeno (µg/m3)")
    no2: float = Field(..., description="Dióxido de nitrógeno (µg/m3)")
    o3: float = Field(..., description="Ozono (µg/m3)")
    so2: float = Field(..., description="Dióxido de azufre (µg/m3)")
    pm2_5: float = Field(..., description="Partículas finas (µg/m3)")
    pm10: float = Field(..., description="Partículas gruesas (µg/m3)")
    nh3: float = Field(..., description="Amoníaco (µg/m3)")


class AirPollutionItem(BaseModel):
    """Modelo para un ítem de contaminación del aire.

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    dt: int = Field(..., description="Fecha y hora de la medición (timestamp)")
    main: AirPollutionMain
    components: AirPollutionComponents


class OpenWeatherAirPollutionResponse(BaseModel):
    """Modelo para la respuesta de contaminación del aire de OpenWeatherMap.

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.

    Returns:
        OpenWeatherAirPollutionResponse: Modelo para la respuesta de contaminación
        del aire de OpenWeatherMap.
    """

    success: bool = Field(..., description="True si la respuesta es exitosa")
    result: List[AirPollutionItem] = Field(
        ..., description="Lista de mediciones de contaminación"
    )
    exception: str = Field("", description="Mensaje de error")
    code: int = Field(0, description="Código de respuesta HTTP")

    @classmethod
    def from_api(cls, data: dict) -> "OpenWeatherAirPollutionResponse":
        """
        Método de clase para crear una instancia de OpenWeatherAirPollutionResponse
        a partir de los datos de la API.

        Args:
            data (dict): Datos de la API.

        Returns:
            OpenWeatherAirPollutionResponse: Modelo para la respuesta de contaminación
            del aire de OpenWeatherMap.
        """
        if "list" in data and isinstance(data["list"], list) and len(data["list"]) > 0:
            items = [AirPollutionItem(**item) for item in data["list"]]
            return cls(success=True, result=items, code=200)
        else:
            return cls(
                success=False,
                result=[],
                exception="Error en la respuesta",
                code=data.get("cod", 0),
            )
