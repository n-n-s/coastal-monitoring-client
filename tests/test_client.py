import datetime as dt
import json

import responses

from coastal_monitoring_client import CMClient
from coastal_monitoring_client.endpoints import BASE_URL
from coastal_monitoring_client.models import Observation
from tests.conftest import DATA_DIR


@responses.activate
def test_observation():
    with (DATA_DIR / "observation_waves.json").open() as f:
        json_data = json.load(f)
    resp_mock = responses.Response(method="GET", url=BASE_URL + "/waves/20250104093000", json=json_data)
    responses.add(resp_mock)

    with CMClient(api_key="anything", referer="anything") as client:
        actual = client.get_observation_of_waves(sensor_name="Porthleven", timestamp=dt.datetime(2025, 1, 4, 9, 30, 0))

    assert isinstance(actual, Observation)

    # check date has been parsed correctly
    assert actual.features[0].properties.date == dt.datetime(2025, 1, 4, 9, 30, 0).replace(tzinfo=dt.UTC)
