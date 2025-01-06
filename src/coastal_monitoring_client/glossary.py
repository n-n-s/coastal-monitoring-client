"""Glossary of wave parameters.

Ref: https://coastalmonitoring.org/ccoresources/waveparameterhandbook/
"""

from enum import Enum
from pprint import pprint

from pydantic import BaseModel, Field


class MeasurementUnits(str, Enum):
    """Measurement units."""

    METRES = "m"
    SECONDS = "s"
    DEGREES_CELCIUS = "°C"
    KW_PER_METRE = "kW/m"
    DEGREES = "°"


class WaveParameter(BaseModel):
    """Represents a wave parameter."""

    abbreviation: str = Field(examples=["hs", "hmax", "tmax"])
    descriptive_name: str = Field(description="Long name", examples=["wave_height_significant_m"])
    measurement_units: MeasurementUnits = Field(description="Measurement units", examples=["m", "s"])
    description: str = Field(
        description="Explanation of the parameter.",
        examples=["Maximum wave height, i.e. largest zero-upcrossing wave."],
    )


class Glossary:
    """Glossary of Wave Parameters.

    Ref: https://coastalmonitoring.org/ccoresources/waveparameterhandbook/
    """

    hs = WaveParameter(
        abbreviation="hs",
        descriptive_name="wave_height_significant_m",
        measurement_units=MeasurementUnits.METRES,
        description="Mean height of the highest 1/3rd of the waves. Significant wave height , statistically-derived.",
    )
    hmax = WaveParameter(
        abbreviation="hs",
        descriptive_name="wave_height_max_m",
        measurement_units=MeasurementUnits.METRES,
        description="Maximum wave height, i.e. largest zero-upcrossing wave.",
    )
    tp = WaveParameter(
        abbreviation="tp",
        descriptive_name="wave_period_peak_s",
        measurement_units=MeasurementUnits.SECONDS,
        description="The peak period. The period associated with the most energetic waves in the wave spectrum.",
    )
    tz = WaveParameter(
        abbreviation="tp",
        descriptive_name="wave_period_mean_s",
        measurement_units=MeasurementUnits.SECONDS,
        description="Mean period of all waves, i.e. the zero-upcross period Tz.",
    )
    te = WaveParameter(
        abbreviation="te",
        descriptive_name="wave_period_energy_equivalent_s",
        measurement_units=MeasurementUnits.SECONDS,
        description=(
            "The period of an energy equivalent regular wave. In other words, the period corresponding to the "
            "weighted average of the wave energy."
        ),
    )
    sst = WaveParameter(
        abbreviation="sst",
        descriptive_name="sea_surface_temperature_degc",
        measurement_units=MeasurementUnits.DEGREES_CELCIUS,
        description="Sea surface temperature.",
    )
    power = WaveParameter(
        abbreviation="power",
        descriptive_name="wave_power_kwperm",
        measurement_units=MeasurementUnits.KW_PER_METRE,
        description="Wave power. The rate of transfer of energy through each metre of wavefront.",
    )
    pdir = WaveParameter(
        abbreviation="pdir",
        descriptive_name="wave_direction_deg",
        measurement_units=MeasurementUnits.DEGREES,
        description=(
            "The wave direction associated with the most energetic waves in the wave spectrum."
            "Also referred to as the peak direction."
        ),
    )
    spread = WaveParameter(
        abbreviation="spread",
        descriptive_name="directional_wave_spread_deg",
        measurement_units=MeasurementUnits.DEGREES,
        description="The directional wave spread at the peak frequency.",
    )

    @classmethod
    def print(cls) -> None:
        """Pretty print the glossary."""
        pprint(
            {
                k: v.model_dump()
                for k, v in cls.__dict__.items()
                if (not k.startswith("_")) and isinstance(v, WaveParameter)
            }
        )

    @classmethod
    def column_mapping(cls) -> dict:
        """Map abbreviation to descriptive_name."""
        return {
            k: v.descriptive_name
            for k, v in cls.__dict__.items()
            if (not k.startswith("_")) and isinstance(v, WaveParameter)
        }

    @classmethod
    def wave_parameter_abbreviations(cls) -> set[str]:
        """Set of all the wave parameter abbreviations that are defined in this Glossary class."""
        return {k for k, v in cls.__dict__.items() if (not k.startswith("_")) and isinstance(v, WaveParameter)}


p = [
    "bounded_by",
    "ms_geometry",
    "ms_geometry_osgb",
    "id",
    "sensor",
    "institution",
    "hs",
    "hmax",
    "sst",
    "type",
    "value",
    "tp",
    "tz",
    "pdir",
    "spread",
    "te",
    "power",
]
