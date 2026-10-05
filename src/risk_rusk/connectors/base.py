"""Connector contracts keep ingestion separate from scoring."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping
from datetime import date
from typing import Any


class PointInTimeConnector(ABC):
    @abstractmethod
    def fetch(self, start: date, end: date) -> Iterable[Mapping[str, Any]]:
        """Yield records published or observable within the requested window."""
        raise NotImplementedError

