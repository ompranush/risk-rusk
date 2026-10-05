from datetime import date
from pathlib import Path

import pytest

from risk_rusk.data import SnapshotStore

DATA = Path(__file__).parents[1] / "data" / "sample" / "company_signals.csv"


def test_point_in_time_lookup_does_not_use_future_snapshot():
    store = SnapshotStore.from_csv(DATA)
    snapshot = store.latest_on_or_before("Northstar Delivery", date(2025, 3, 1))
    assert snapshot.as_of == date(2025, 1, 1)


def test_lookup_before_first_snapshot_fails():
    store = SnapshotStore.from_csv(DATA)
    with pytest.raises(LookupError):
        store.latest_on_or_before("Northstar Delivery", date(2024, 12, 31))

