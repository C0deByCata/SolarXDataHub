"""File containing the Solax Cloud API model."""

from typing import Optional

from pydantic import BaseModel


class SolaxCloudResult(BaseModel):
    """Model for the Solax Cloud API real-time data response.

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    inverterSN: str
    sn: str
    acpower: float
    yieldtoday: float
    yieldtotal: float
    feedinpower: float
    feedinenergy: float
    consumeenergy: float
    feedinpowerM2: Optional[float] = None
    soc: Optional[float] = None
    peps1: Optional[float] = None
    peps2: Optional[float] = None
    peps3: Optional[float] = None
    inverterType: str
    inverterStatus: str
    uploadTime: str  # Formato "YYYY-MM-DD HH:MM:SS"
    batPower: Optional[float] = None
    powerdc1: float
    powerdc2: float
    powerdc3: Optional[float] = None
    powerdc4: Optional[float] = None
    batStatus: Optional[str] = None
    utcDateTime: str  # Formato "YYYY-MM-DDTHH:MM:SSZ"


class SolaxCloudResponse(BaseModel):
    """Model for the Solax Cloud API response.

    Args:
        BaseModel (pydantic.BaseModel): Base model for Pydantic.
    """

    success: bool
    exception: str
    result: Optional[SolaxCloudResult] = None
    code: int
