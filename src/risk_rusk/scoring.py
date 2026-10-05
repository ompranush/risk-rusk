"""Transparent weighted scoring baseline for the MVP."""

from __future__ import annotations

from dataclasses import dataclass

from risk_rusk.domain import Contribution, RiskQuery, SignalSnapshot

WEIGHTS = {
    "company_restructuring": 0.28,
    "hiring_slowdown": 0.18,
    "financial_pressure": 0.16,
    "sector_redundancies": 0.16,
    "regional_redundancies": 0.08,
    "role_exposure": 0.14,
}

LABELS = {
    "company_restructuring": "Company restructuring signal",
    "hiring_slowdown": "Hiring slowdown",
    "financial_pressure": "Financial pressure",
    "sector_redundancies": "Sector redundancy activity",
    "regional_redundancies": "Regional redundancy activity",
    "role_exposure": "Role exposure",
}


@dataclass(frozen=True)
class RiskAssessment:
    score: int
    band: str
    confidence: str
    contributions: tuple[Contribution, ...]
    evidence: tuple[str, ...]
    snapshot_date: str
    source_kind: str


class RiskEngine:
    """Deterministic baseline that can be backtested before introducing ML."""

    def score(self, query: RiskQuery, snapshot: SignalSnapshot) -> RiskAssessment:
        del query  # Reserved for role/location-specific feature joins in production.
        contributions = tuple(
            Contribution(
                key=key,
                label=LABELS[key],
                value=getattr(snapshot, key),
                weight=weight,
                points=getattr(snapshot, key) * weight,
            )
            for key, weight in WEIGHTS.items()
        )
        score = round(sum(item.points for item in contributions))
        score = max(0, min(100, score))
        return RiskAssessment(
            score=score,
            band=self._band(score),
            confidence="Demo only" if snapshot.source_kind == "sample" else "Experimental",
            contributions=tuple(sorted(contributions, key=lambda item: item.points, reverse=True)),
            evidence=snapshot.evidence,
            snapshot_date=snapshot.as_of.isoformat(),
            source_kind=snapshot.source_kind,
        )

    @staticmethod
    def _band(score: int) -> str:
        if score < 30:
            return "Lower"
        if score < 55:
            return "Moderate"
        if score < 75:
            return "Elevated"
        return "High"

