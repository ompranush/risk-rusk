from datetime import UTC, date, datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from risk_rusk.data import SnapshotStore
from risk_rusk.domain import RiskQuery
from risk_rusk.scoring import RiskEngine

ROOT = Path(__file__).parent
SAMPLE_DATA = ROOT / "data" / "sample" / "company_signals.csv"

st.set_page_config(page_title="Risk Rusk", page_icon="🛡️", layout="wide")
st.title("🛡️ Risk Rusk")
st.caption("A free, interpretable UK redundancy-risk predictor — sample-data MVP")

st.warning(
    "Demo mode: every signal shown here is fictional sample data. This is not employment, "
    "legal, or financial advice and does not predict whether an individual will lose their job."
)

store = SnapshotStore.from_csv(SAMPLE_DATA)

with st.sidebar:
    st.header("Your scenario")
    company = st.selectbox("Company", store.companies())
    role = st.text_input("Role", "Analytics Engineer")
    location = st.selectbox("Location", ["London", "South East", "North West", "Scotland", "Other UK"])
    department = st.selectbox("Department", ["Technology", "Operations", "Finance", "Sales", "Other"])
    seniority = st.selectbox("Seniority", ["Entry", "Mid-level", "Senior", "Manager", "Director+"])
    as_of = st.date_input(
        "As of", value=date(2025, 7, 1), max_value=datetime.now(UTC).date()
    )

query = RiskQuery(company, role, location, department, seniority, as_of)

try:
    snapshot = store.latest_on_or_before(company, as_of)
except LookupError as exc:
    st.error(str(exc))
    st.stop()

assessment = RiskEngine().score(query, snapshot)

score_col, band_col, date_col = st.columns(3)
score_col.metric("Redundancy risk score", f"{assessment.score} / 100")
band_col.metric("Risk band", assessment.band)
date_col.metric("Signal snapshot", assessment.snapshot_date)
st.progress(assessment.score / 100)

st.subheader("What drives the score")
frame = pd.DataFrame(
    {
        "Signal": [item.label for item in assessment.contributions],
        "Signal level": [item.value for item in assessment.contributions],
        "Weight": [f"{item.weight:.0%}" for item in assessment.contributions],
        "Points": [round(item.points, 1) for item in assessment.contributions],
    }
)
st.dataframe(frame, hide_index=True, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Illustrative evidence")
    for evidence in assessment.evidence:
        st.write(f"• {evidence}")
with right:
    st.subheader("How to read this")
    st.write(
        "The score is a weighted summary of company, hiring, financial, sector, regional, "
        "and role signals. Each input uses the latest snapshot available on or before the "
        "selected date, which prevents future information leaking into later backtests."
    )

with st.expander("Method and limitations"):
    st.markdown(
        """
        - The current weights are transparent product hypotheses, not trained parameters.
        - Sample companies and evidence are fictional and deliberately labelled.
        - A company-level signal cannot account for team performance, protected characteristics,
          consultation outcomes, or individual employment decisions.
        - Production claims require source attribution, data quality checks, calibration, and
          historical out-of-time validation.
        """
    )
