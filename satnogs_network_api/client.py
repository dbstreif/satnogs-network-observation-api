"""SatNOGS Network API client."""

import requests

from satnogs_network_api.resources import Observations, Stations, Transmitters

DEFAULT_BASE_URL = "https://network.satnogs.org"


class SatnogsNetworkClient:
    """Client for the SatNOGS Network Observation API.

    All endpoints are read-only and publicly accessible. No authentication
    is required.

    Args:
        base_url: Base URL for the SatNOGS Network instance.
            Defaults to https://network.satnogs.org.
    """

    def __init__(self, base_url: str = DEFAULT_BASE_URL) -> None:
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers["Accept"] = "application/json"

        self.observations = Observations(self._session, self._base_url)
        self.stations = Stations(self._session, self._base_url)
        self.transmitters = Transmitters(self._session, self._base_url)

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self._session.close()

    def __enter__(self) -> "SatnogsNetworkClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()
