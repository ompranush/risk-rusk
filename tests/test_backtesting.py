import pytest

from risk_rusk.backtesting import brier_score


def test_brier_score():
    assert brier_score([0.8, 0.2], [True, False]) == pytest.approx(0.04)


def test_brier_score_rejects_invalid_inputs():
    with pytest.raises(ValueError):
        brier_score([], [])

