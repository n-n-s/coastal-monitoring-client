"""Model definitions."""

import datetime as dt
import logging
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from pydantic.alias_generators import to_camel

from coastal_monitoring_client.endpoints import Endpoints

logger = logging.getLogger(__name__)


class BaseModelExtension(BaseModel):
    """Extend pydantic BaseModel."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


def _parse_datetime(value: str) -> dt.datetime:
    return dt.datetime.strptime(value, "%Y%m%d#%H%M%S")


class PropertiesWave(BaseModelExtension):
    """Holds measurement details (Properties is found within the Feature endpoint)."""

    bounded_by: Any | None = None
    ms_geometry: Any | None = None
    ms_geometry_osgb: Any | None = None
    id: str = Field(description="Unique identifier for sensor.", examples=["107"])
    sensor: str = Field(description="Name of sensor.", examples=["Porthleven"])
    institution: str
    date: Annotated[dt.datetime, BeforeValidator(_parse_datetime)]
    hs: float
    hmax: float
    sst: float
    type: Endpoints
    value: float
    tp: float
    tz: float
    pdir: float
    spread: float
    te: float
    power: float


class Geometry(BaseModelExtension):
    """Holds location details (Geometry is found within the Feature endpoint)."""

    type: str
    coordinates: tuple[float, float] = Field(description="Tuple of latitude and longitude")


class Feature(BaseModelExtension):
    """Represents a Feature (which is found within the Observation endpoint)."""

    type: str
    id: str = Field(examples=["waves.107"])
    properties: PropertiesWave
    geometry: Geometry


class Observation(BaseModelExtension):
    """Represents a response from an Observation endpoint."""

    type: str
    features: list[Feature]
