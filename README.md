# Risk Rusk

Risk Rusk is a free, interpretable UK redundancy-risk predictor. The MVP estimates
**company-level risk**, explains every point in the score, and is deliberately structured for
historical backtesting before any machine-learning model is introduced.

> **Important:** the included dataset is fictional sample data. The app does not predict whether
> a particular person will lose their job and is not employment, legal, or financial advice.

## What works today

- A Streamlit scenario form for company, role, location, department, seniority and date.
- A deterministic 0–100 score with six visible, weighted contributions.
- Point-in-time snapshot selection: a prediction can only see information available on or before
  its `as_of` date.
- Sample company histories that make the demo runnable without credentials or fabricated claims.
- A small backtesting module with a calibration metric, ready for labelled historical events.
- Tests for score behaviour, point-in-time correctness and evaluation utilities.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
streamlit run app.py
```

Run checks with:

```bash
pytest -q
ruff check .
```

## Score design

The first baseline is intentionally boring and auditable:

| Signal | Weight |
|---|---:|
| Company restructuring | 28% |
| Hiring slowdown | 18% |
| Financial pressure | 16% |
| Sector redundancy activity | 16% |
| Role exposure | 14% |
| Regional redundancy activity | 8% |

Every feature is normalised to a 0–100 risk scale. The score is the weighted sum, clamped to
0–100. These weights are product hypotheses—not learned parameters—and must be calibrated against
historical outcomes before production use.

## Architecture

```text
data sources -> point-in-time connectors -> normalised snapshots -> scoring model -> UI/API
                                                       |                |
                                                       +-> labels ------+-> backtests
```

```text
app.py                         Streamlit UI
data/sample/                   Explicitly fictional demo snapshots
src/risk_rusk/domain.py        Typed point-in-time records
src/risk_rusk/data.py          CSV snapshot repository
src/risk_rusk/scoring.py       Explainable baseline model
src/risk_rusk/backtesting.py   Evaluation primitives
src/risk_rusk/connectors/      Contracts and source roadmap
tests/                         Unit tests
```

Keeping immutable dated snapshots is essential: it prevents future information from leaking into
historical predictions. A later ML model should implement the same scoring interface so that the
UI and evaluation pipeline remain stable.

## Real-data roadmap

No production records, API keys, or source claims are included. Proposed connectors are separate
from sample data and should preserve publication date, observation date, provenance and licence.

1. **HR1 / ONS** — ingest official aggregate redundancy statistics by industry and region. Confirm
   the current download/API format and release calendar, preserve revisions, and never present
   aggregates as named-company filings.
2. **layoffs.uk** — ingest attributable named-employer events under its published licence terms;
   retain announcement status, source URL and attribution. Review schema and terms before coding.
3. **Companies House** — use the official API for accounts and filing metadata. Store credentials
   outside the repository and engineer lag-aware financial-distress features.
4. **Adzuna** — use a licensed API and secrets management to build vacancy-trend features by
   employer, occupation and geography. Do not scrape or commit credentials.
5. **Public company/news signals** — restrict collection to attributable company releases,
   regulatory filings and licensed/public news. Store URL, publisher and publication timestamp;
   deduplicate and separate facts from extracted language signals.

## Backtesting and ML path

1. Define a label such as a public UK redundancy announcement within 180 days of prediction.
2. Build monthly feature snapshots with strict `available_at <= prediction_date` checks.
3. Split chronologically, with company grouping where appropriate; never random-split event rows.
4. Report precision/recall at operational thresholds, PR-AUC, Brier score, calibration curves and
   coverage. Compare every model with this transparent baseline.
5. Start with regularised logistic regression or gradient boosting plus calibrated probabilities.
   Keep per-prediction reason codes and monitor sector/company-size bias and drift.

## Licence

MIT for the code. Upstream datasets retain their own licences and attribution requirements.
