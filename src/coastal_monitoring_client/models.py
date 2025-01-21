"""Model definitions."""

import datetime as dt
import logging
from typing import Annotated, Any

import pandas as pd
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from pydantic.alias_generators import to_camel

from coastal_monitoring_client.endpoints import Endpoints
from coastal_monitoring_client.glossary import Glossary

logger = logging.getLogger(__name__)


class BaseModelExtension(BaseModel):
    """Extend pydantic BaseModel."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


def _parse_datetime(value: str) -> dt.datetime:
    return dt.datetime.strptime(value, "%Y%m%d#%H%M%S").replace(tzinfo=dt.UTC)


class PropertiesWave(BaseModelExtension):
    """Holds measurement details (Properties is found within the Feature endpoint)."""

    bounded_by: Any | None = None
    ms_geometry: Any | None = None
    ms_geometry_osgb: Any | None = None
    id: str = Field(description="Unique identifier for sensor.", examples=["107"])
    sensor: str = Field(description="Name of sensor.", examples=["Porthleven"])
    institution: str
    date: Annotated[dt.datetime, BeforeValidator(_parse_datetime)]
    hs: Annotated[float | None, BeforeValidator(eval)]
    hmax: Annotated[float | None, BeforeValidator(eval)]
    sst: Annotated[float | None, BeforeValidator(eval)]
    type: Endpoints
    value: Annotated[float | None, BeforeValidator(eval)]
    tp: Annotated[float | None, BeforeValidator(eval)]
    tz: Annotated[float | None, BeforeValidator(eval)]
    pdir: Annotated[float | None, BeforeValidator(eval)]
    spread: Annotated[float | None, BeforeValidator(eval)]
    te: Annotated[float | None, BeforeValidator(eval)]
    power: Annotated[float | None, BeforeValidator(eval)]

    def to_dataframe(self) -> pd.DataFrame:
        """Time series of feature properties data with `date` as a pd.DatetimeIndex."""
        return pd.DataFrame(self.model_dump(exclude={"date"}), index=[self.date])


class Coordinates(BaseModel):
    """Lat and lon."""

    latitude: float
    longitude: float


def _parse_latitude_and_longitude(value: tuple[float, float]) -> Coordinates:
    return Coordinates(latitude=value[1], longitude=value[0])


class Geometry(BaseModelExtension):
    """Holds location details (Geometry is found within the Feature endpoint)."""

    type: str
    coordinates: Annotated[Coordinates, BeforeValidator(_parse_latitude_and_longitude)]


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

    def feature_properties_to_dataframe(self, use_descriptive_column_names: bool = True) -> pd.DataFrame:
        """Time series of feature properties data.

        :param use_descriptive_column_names: if true then maps to more descriptive column names using a Glossary.
        :return: time series of feature properties data
        """
        df_list = []
        for feature in self.features:
            df_list.append(feature.properties.to_dataframe())
        _df = pd.concat(df_list).sort_index()
        if use_descriptive_column_names:
            _df = _df.rename(columns=Glossary.column_mapping())
        return _df
