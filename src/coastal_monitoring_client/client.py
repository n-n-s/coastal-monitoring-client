"""Client definition."""

import datetime as dt
import logging

import requests

from coastal_monitoring_client.endpoints import BASE_URL, Endpoints
from coastal_monitoring_client.models import Observation

logger = logging.getLogger(__name__)


class CMClient:
    """Coastal Monitoring API client."""

    def __init__(self, api_key: str, referer: str):
        """Initialise client instance.

        :param api_key: your personal API Key
        :param referer: web domain registered for your personal API Key
        """
        self._api_key = api_key
        self._referer = referer
        self._client = None

    def __enter__(self):
        """Context management."""
        self._session = requests.Session()
        self._session.headers.update(
            {"X-API-Key": self._api_key, "Referer": self._referer, "Accept": "application/json"}
        )
        logger.debug("Session created")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context management."""
        self._session.close()
        logger.debug("Session closed")

    def get_observation_of_waves(self, sensor_name: str, timestamp: dt.datetime) -> Observation:
        """Response from a GET request to the Observations endpoint.

        :param sensor_name: e.g. 'Porthleven'.
        :param timestamp: datetime of the request. The observation closest to this time is returned.
        :return: response.
        """
        _url = BASE_URL + f"/{Endpoints.WAVES.value}/{timestamp.strftime('%Y%m%d%H%M%S')}"
        _params = {"sensor": sensor_name}
        resp = self._session.get(url=_url, params=_params)
        resp.raise_for_status()
        return Observation.model_validate(resp.json())
