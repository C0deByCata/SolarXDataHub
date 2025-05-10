"""File containing the WeatherbitResponse model."""

from typing import Optional

from pydantic import BaseModel, Field


class WeatherDescription(BaseModel):
    """
    Modelo que describe las características del clima.

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    icon: str = Field(..., description="Código del icono meteorológico")
    description: str = Field(..., description="Descripción del clima")
    code: int = Field(..., description="Código del clima")


class WeatherDataResult(BaseModel):
    """
    Modelo que describe los datos meteorológicos.

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    wind_cdir: str = Field(..., description="Dirección del viento (abreviada)")
    rh: int = Field(..., description="Humedad relativa (%)")
    pod: str = Field(..., description="Período del día (d = día, n = noche)")
    lon: float = Field(..., description="Longitud")
    pres: float = Field(..., description="Presión atmosférica en mb")
    timezone: str = Field(..., description="Zona horaria")
    ob_time: str = Field(..., description="Tiempo de observación (YYYY-MM-DD HH:MM)")
    country_code: str = Field(..., description="Código del país")
    clouds: int = Field(..., description="Porcentaje de nubes")
    vis: float = Field(..., description="Visibilidad en km")
    wind_spd: float = Field(..., description="Velocidad del viento (m/s)")
    gust: float = Field(..., description="Velocidad de ráfagas del viento (m/s)")
    wind_cdir_full: str = Field(..., description="Dirección completa del viento")
    app_temp: float = Field(..., description="Temperatura aparente en °C")
    state_code: str = Field(..., description="Código de estado")
    ts: int = Field(..., description="Timestamp Unix")
    h_angle: float = Field(..., description="Ángulo horario solar")
    dewpt: float = Field(..., description="Punto de rocío en °C")
    weather: WeatherDescription = Field(..., description="Información del clima")
    uv: float = Field(..., description="Índice UV")
    aqi: int = Field(..., description="Índice de calidad del aire")
    station: str = Field(..., description="Estación meteorológica")
    sources: list[str] = Field(
        ..., description="Fuentes de datos (lista de identificadores)"
    )
    wind_dir: int = Field(..., description="Dirección del viento en grados")
    elev_angle: float = Field(..., description="Ángulo de elevación solar")
    datetime: str = Field(
        ..., description="Fecha y hora del reporte (formato: YYYY-MM-DD:HH)"
    )
    precip: float = Field(..., description="Precipitación en mm")
    ghi: float = Field(..., description="Irradiancia horizontal global (W/m2)")
    dni: float = Field(..., description="Irradiancia normal directa (W/m2)")
    dhi: float = Field(..., description="Irradiancia difusa horizontal (W/m2)")
    solar_rad: float = Field(..., description="Radiación solar (W/m2)")
    city_name: str = Field(..., description="Nombre de la ciudad")
    sunrise: str = Field(..., description="Hora de salida del sol (HH:MM)")
    sunset: str = Field(..., description="Hora de puesta del sol (HH:MM)")
    temp: float = Field(..., description="Temperatura en °C")
    lat: float = Field(..., description="Latitud")
    slp: float = Field(..., description="Presión a nivel del mar en mb")
    snow: float = Field(..., description="Cantidad de nieve")


class WeatherbitResponse(BaseModel):
    """
    Modelo adaptado para la respuesta de Weatherbit con una estructura similar a SolaxCloudResponse.
    """

    success: bool = Field(..., description="True si la petición fue exitosa")
    exception: str = Field("", description="Mensaje de error, en caso de haberlo")
    result: Optional[WeatherDataResult] = Field(
        None, description="Primer registro de datos meteorológicos"
    )
    code: int = Field(0, description="Código de respuesta, 0 si todo está bien")

    @classmethod
    def from_api(cls, data: dict) -> "WeatherbitResponse":
        """
        Crea una instancia de WeatherbitResponse a partir de la respuesta original de la API.
        Si 'data' tiene contenido en la clave 'data', se considera exitosa.
        """
        if data.get("data") and len(data["data"]) > 0:
            return cls(
                success=True,
                exception="",
                result=WeatherDataResult(**data["data"][0]),
                code=0,
            )
        else:
            return cls(
                success=False, exception="No se recibieron datos", result=None, code=1
            )
