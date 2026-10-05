from datetime import date

from risk_rusk.domain import RiskQuery, SignalSnapshot
from risk_rusk.scoring import WEIGHTS, RiskEngine


def test_weights_sum_to_one():
    assert sum(WEIGHTS.values()) == 1


def test_score_is_weighted_and_explainable():
    snapshot = SignalSnapshot(
        company="Example",
        as_of=date(2025, 1, 1),
        sector="Technology",
        company_restructuring=100,
        hiring_slowdown=0,
        financial_pressure=0,
        sector_redundancies=0,
        regional_redundancies=0,
        role_exposure=0,
    )
    query = RiskQuery("Example", "Engineer", "London", "Technology", "Senior", date(2025, 1, 1))
    result = RiskEngine().score(query, snapshot)
    assert result.score == 28
    assert result.band == "Lower"
    assert result.contributions[0].key == "company_restructuring"


def test_score_is_clamped():
    values = {
        "company_restructuring": 150,
        "hiring_slowdown": 150,
        "financial_pressure": 150,
        "sector_redundancies": 150,
        "regional_redundancies": 150,
        "role_exposure": 150,
    }
    snapshot = SignalSnapshot("Example", date(2025, 1, 1), "Other", **values)
    query = RiskQuery("Example", "Role", "UK", "Other", "Senior", date(2025, 1, 1))
    assert RiskEngine().score(query, snapshot).score == 100
