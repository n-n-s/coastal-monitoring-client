"""Known available endpoints on the Coastal Monitoring API."""

from enum import Enum

BASE_URL = "https://coastalmonitoring.org/observations"


class Endpoints(str, Enum):
    """Available API endpoints."""

    WAVES = "waves"
    TIDES = "tides"
    TIDE_PREDICTIONS = "tidepredictions"
    MET = "met"
