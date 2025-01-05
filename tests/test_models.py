import datetime as dt
import json

import pandas as pd

from coastal_monitoring_client.glossary import Glossary
from coastal_monitoring_client.models import Coordinates, Observation
from tests.conftest import DATA_DIR


def _load_observation():
    with (DATA_DIR / "observation_waves.json").open() as f:
        return Observation.model_validate(json.load(f))


def test_lat_lon_parsing():
    obs = _load_observation()
    location = obs.features[0].geometry.coordinates

    assert isinstance(location, Coordinates)
    assert location.latitude == 50.06223
    assert location.longitude == -5.30745


def test_datetime_parsing():
    obs = _load_observation()
    timestamp = obs.features[0].properties.date

    assert timestamp.tzinfo == dt.UTC
    assert timestamp.tzname() == "UTC"


def test_to_dataframe():
    with (DATA_DIR / "observation_waves.json").open() as f:
        obs = Observation.model_validate(json.load(f))

    # check columns are mapped
    actual = obs.feature_properties_to_dataframe()
    mapped_columns = set(Glossary.column_mapping().values())
    assert set(actual.columns).intersection(mapped_columns) == mapped_columns

    # check columns are raw
    actual = obs.feature_properties_to_dataframe(use_descriptive_column_names=False)
    mapped_columns = set(Glossary.column_mapping().values())
    assert set(actual.columns).intersection(mapped_columns) == set()

    # construct expected
    feature_properties = obs.features[0].properties
    expected = pd.DataFrame(feature_properties.model_dump(exclude={"date"}), index=[feature_properties.date])

    # check dataframe values
    pd.testing.assert_frame_equal(actual, expected)
