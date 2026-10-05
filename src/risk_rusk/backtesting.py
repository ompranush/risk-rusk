"""Minimal time-aware backtesting primitives for future labelled events."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class LabelledOutcome:
    company: str
    prediction_date: date
    event_within_180_days: bool


def brier_score(predictions: list[float], outcomes: list[bool]) -> float:
    """Return mean squared probability error; lower is better."""
    if not predictions or len(predictions) != len(outcomes):
        raise ValueError("Predictions and outcomes must have the same non-zero length")
    if any(not 0 <= prediction <= 1 for prediction in predictions):
        raise ValueError("Predictions must be probabilities between 0 and 1")
    return sum((prediction - int(outcome)) ** 2 for prediction, outcome in zip(predictions, outcomes)) / len(predictions)

