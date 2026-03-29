"""Lazy cursor-based pagination for the SatNOGS Network API."""

from typing import Any, Callable, Dict, Iterator, List, Optional, Type, TypeVar
from urllib.parse import parse_qs, urlparse

import requests

from satnogs_network_api.models import BaseModel

T = TypeVar("T", bound=BaseModel)


class PageIterator(Iterator[T]):
    """Lazy iterator that fetches pages on demand from the SatNOGS Network API.

    Yields typed pydantic model instances by default. Use .json() to get
    an iterator that yields raw dicts instead.
    """

    def __init__(
        self,
        session: requests.Session,
        url: str,
        params: Dict[str, Any],
        model: Type[T],
    ) -> None:
        self._session = session
        self._url = url
        self._params = params
        self._model = model
        self._buffer: List[Any] = []
        self._next_url: Optional[str] = url
        self._next_params: Optional[Dict[str, Any]] = params
        self._raw_mode = False
        self._exhausted = False

    def json(self) -> "PageIterator[T]":
        """Return an iterator that yields raw dicts instead of model instances."""
        clone = PageIterator(
            session=self._session,
            url=self._url,
            params=self._params,
            model=self._model,
        )
        clone._raw_mode = True
        return clone

    def _fetch_page(self) -> None:
        if self._next_url is None:
            self._exhausted = True
            return

        response = self._session.get(self._next_url, params=self._next_params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "results" in data:
            self._buffer = data["results"]
            self._next_url = data.get("next")
            self._next_params = None
        elif isinstance(data, list):
            self._buffer = data
            self._next_url = None
            self._next_params = None
        else:
            self._buffer = []
            self._next_url = None
            self._next_params = None

        if not self._buffer:
            self._exhausted = True

    def __next__(self) -> T:
        if not self._buffer and not self._exhausted:
            self._fetch_page()

        if not self._buffer:
            raise StopIteration

        item = self._buffer.pop(0)

        if self._raw_mode:
            return item

        return self._model.model_validate(item)

    def __iter__(self) -> "PageIterator[T]":
        return self
