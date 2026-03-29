"""Tests for resource classes (Observations, Stations, Transmitters)."""

from datetime import datetime
from unittest.mock import MagicMock

from satnogs_network_api.models import Observation, Station, Transmitter
from satnogs_network_api.pagination import PageIterator

from tests.conftest import (
    SAMPLE_OBSERVATION,
    SAMPLE_STATION,
    SAMPLE_TRANSMITTER,
    make_paginated_response,
    mock_response,
)


class TestObservationsResource:
    def test_list_returns_page_iterator(self, client):
        result = client.observations.list()
        assert isinstance(result, PageIterator)

    def test_list_no_filters(self, client):
        data = make_paginated_response([SAMPLE_OBSERVATION])
        client._mock_session.get.return_value = mock_response(data)

        results = list(client.observations.list())
        assert len(results) == 1
        assert results[0].id == 13687665

        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/observations/",
            params={},
        )

    def test_list_with_status_filter(self, client):
        data = make_paginated_response([SAMPLE_OBSERVATION])
        client._mock_session.get.return_value = mock_response(data)

        list(client.observations.list(status="good"))

        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/observations/",
            params={"status": "good"},
        )

    def test_list_with_norad_cat_id(self, client):
        data = make_paginated_response([SAMPLE_OBSERVATION])
        client._mock_session.get.return_value = mock_response(data)

        list(client.observations.list(norad_cat_id=25544))

        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/observations/",
            params={"norad_cat_id": 25544},
        )

    def test_list_with_transmitter_mode(self, client):
        data = make_paginated_response([SAMPLE_OBSERVATION])
        client._mock_session.get.return_value = mock_response(data)

        list(client.observations.list(transmitter_mode="AFSK"))

        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/observations/",
            params={"transmitter_mode": "AFSK"},
        )

    def test_list_with_datetime_filters(self, client):
        data = make_paginated_response([SAMPLE_OBSERVATION])
        client._mock_session.get.return_value = mock_response(data)

        start = datetime(2026, 1, 1)
        end = datetime(2026, 2, 1)
        list(client.observations.list(start=start, start__lt=end))

        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/observations/",
            params={
                "start": "2026-01-01T00:00:00",
                "start__lt": "2026-02-01T00:00:00",
            },
        )

    def test_list_with_bool_filter(self, client):
        data = make_paginated_response([SAMPLE_OBSERVATION])
        client._mock_session.get.return_value = mock_response(data)

        list(client.observations.list(waterfall_status=True))

        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/observations/",
            params={"waterfall_status": "true"},
        )

    def test_list_with_multiple_filters(self, client):
        data = make_paginated_response([SAMPLE_OBSERVATION])
        client._mock_session.get.return_value = mock_response(data)

        list(client.observations.list(
            status="good",
            norad_cat_id=25544,
            ground_station=42,
            transmitter_mode="AFSK",
        ))

        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/observations/",
            params={
                "status": "good",
                "norad_cat_id": 25544,
                "ground_station": 42,
                "transmitter_mode": "AFSK",
            },
        )

    def test_list_none_filters_excluded(self, client):
        data = make_paginated_response([SAMPLE_OBSERVATION])
        client._mock_session.get.return_value = mock_response(data)

        list(client.observations.list(status="good", norad_cat_id=None))

        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/observations/",
            params={"status": "good"},
        )

    def test_get_single(self, client):
        client._mock_session.get.return_value = mock_response(SAMPLE_OBSERVATION)

        obs = client.observations.get(13687665)

        assert isinstance(obs, Observation)
        assert obs.id == 13687665
        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/observations/13687665/"
        )


class TestStationsResource:
    def test_list_returns_page_iterator(self, client):
        result = client.stations.list()
        assert isinstance(result, PageIterator)

    def test_list_no_filters(self, client):
        # Stations API returns a plain list, not paginated
        client._mock_session.get.return_value = mock_response([SAMPLE_STATION])

        results = list(client.stations.list())
        assert len(results) == 1
        assert results[0].id == 26

    def test_list_with_status(self, client):
        client._mock_session.get.return_value = mock_response([SAMPLE_STATION])

        list(client.stations.list(status="online"))

        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/stations/",
            params={"status": "online"},
        )

    def test_get_single(self, client):
        client._mock_session.get.return_value = mock_response(SAMPLE_STATION)

        station = client.stations.get(26)

        assert isinstance(station, Station)
        assert station.id == 26
        assert station.name == "SV1IYO/A"
        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/stations/26/"
        )


class TestTransmittersResource:
    def test_list_returns_page_iterator(self, client):
        result = client.transmitters.list()
        assert isinstance(result, PageIterator)

    def test_list(self, client):
        # Transmitters API returns a plain list
        client._mock_session.get.return_value = mock_response([SAMPLE_TRANSMITTER])

        results = list(client.transmitters.list())
        assert len(results) == 1
        assert results[0].uuid == "MZgyEeYrdJsLnHCt3je6Ed"

    def test_get_single(self, client):
        client._mock_session.get.return_value = mock_response(SAMPLE_TRANSMITTER)

        tx = client.transmitters.get("MZgyEeYrdJsLnHCt3je6Ed")

        assert isinstance(tx, Transmitter)
        assert tx.uuid == "MZgyEeYrdJsLnHCt3je6Ed"
        assert tx.stats.total_count == 6
        client._mock_session.get.assert_called_once_with(
            "https://network.satnogs.org/api/transmitters/MZgyEeYrdJsLnHCt3je6Ed"
        )
