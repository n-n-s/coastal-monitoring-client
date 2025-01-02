# coastal-monitoring-client
Python client for the [Coastal Monitoring API](https://coastalmonitoring.org/ccoresources/api/).

You will need contact Coastal Monitoring to request a personal API Key and specify a domain for API requests.
*(Fill in and submit the form at the bottom of the [webpage](https://coastalmonitoring.org/ccoresources/api/))*

## Usage

Example of getting the most recent observations for the Porthleven sensor:

```python
import datetime as dt

from coastal_monitoring_client.client import CMClient

with CMClient(
        api_key="your-personal-api-key",
        referer="your-referer-for-your-personal-api-key",  # e.g. "http://www.yourdomain.com"
) as client:
    obs = client.get_observation_of_waves(sensor_name="Porthleven", timestamp=dt.datetime.now())
```
