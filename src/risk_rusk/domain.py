"""Typed domain objects shared by ingestion, scoring, and backtesting."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RiskQuery:
    company: str
    role: str
    location: str
    department: str
    seniority: str
    as_of: date


@dataclass(frozen=True)
class SignalSnapshot:
    """Point-in-time feature values on a common 0–100 risk scale."""

    company: str
    as_of: date
    sector: str
    company_restructuring: float
    hiring_slowdown: float
    financial_pressure: float
    sector_redundancies: float
    regional_redundancies: float
    role_exposure: float
    evidence: tuple[str, ...] = ()
    source_kind: str = "sample"


@dataclass(frozen=True)
class Contribution:
    key: str
    label: str
    value: float
    weight: float
    points: float

