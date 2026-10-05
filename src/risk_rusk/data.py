"""Data access with explicit point-in-time semantics."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from risk_rusk.domain import SignalSnapshot

NUMERIC_FIELDS = (
    "company_restructuring",
    "hiring_slowdown",
    "financial_pressure",
    "sector_redundancies",
    "regional_redundancies",
    "role_exposure",
)


class SnapshotStore:
    """Small CSV-backed store; replaceable with a warehouse later."""

    def __init__(self, snapshots: list[SignalSnapshot]):
        self._snapshots = snapshots

    @classmethod
    def from_csv(cls, path: str | Path) -> SnapshotStore:
        snapshots: list[SignalSnapshot] = []
        with Path(path).open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                snapshots.append(
                    SignalSnapshot(
                        company=row["company"],
                        as_of=date.fromisoformat(row["as_of"]),
                        sector=row["sector"],
                        evidence=tuple(filter(None, row["evidence"].split("|"))),
                        source_kind=row.get("source_kind", "sample"),
                        **{field: float(row[field]) for field in NUMERIC_FIELDS},
                    )
                )
        return cls(snapshots)

    def companies(self) -> list[str]:
        return sorted({snapshot.company for snapshot in self._snapshots})

    def latest_on_or_before(self, company: str, as_of: date) -> SignalSnapshot:
        candidates = [
            snapshot
            for snapshot in self._snapshots
            if snapshot.company.casefold() == company.casefold() and snapshot.as_of <= as_of
        ]
        if not candidates:
            raise LookupError(f"No snapshot for {company!r} on or before {as_of.isoformat()}")
        return max(candidates, key=lambda snapshot: snapshot.as_of)

