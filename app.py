import json
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="SupeRR Selector | Pressure Analytics", page_icon="🏏", layout="wide")
ROOT = Path(__file__).parent

@st.cache_data
def load_csv(name):
    return pd.read_csv(ROOT / name)

bat_top = load_csv("top10_batters.csv")
bowl_top = load_csv("top10_bowlers.csv")
bat_all = load_csv("all_batter_scores.csv")
bowl_all = load_csv("all_bowler_scores.csv")
sensitivity = load_csv("sensitivity_analysis.csv")
audit = json.loads((ROOT / "audit_summary.json").read_text(encoding="utf-8"))

st.title("🏏 SupeRR Selector Season 2")
st.caption("Round 1 — Reliability under pressure | Official organizer-supplied IPL + T20I data")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Matches analysed", f'{audit["analysis_matches"]:,}')
c2.metric("Deliveries analysed", f'{audit["analysis_deliveries"]:,}')
c3.metric("Eligible batters", f'{audit["eligible_batters_60_balls_8_innings"]:,}')
c4.metric("Eligible bowlers", f'{audit["eligible_bowlers_60_balls_8_innings"]:,}')

st.info(
    f'Data window: {audit["date_min"]} to {audit["date_max"]} | '
    f'IPL: {audit["IPL_matches"]} matches | T20I: {audit["T20I_matches"]} matches'
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Top 10 Batters", "Top 10 Bowlers", "All Eligible Players", "Sensitivity"]
)

with tab1:
    st.subheader("Most reliable batters under pressure")
    st.bar_chart(bat_top.set_index("player")["score"])
    st.dataframe(
        bat_top[["rank", "player", "score", "pressure_runs", "pressure_balls",
                 "pressure_avg", "pressure_sr", "base_sr", "pressure_innings", "formats"]],
        use_container_width=True, hide_index=True
    )

with tab2:
    st.subheader("Most reliable bowlers under pressure")
    st.bar_chart(bowl_top.set_index("player")["score"])
    st.dataframe(
        bowl_top[["rank", "player", "score", "pressure_wickets", "pressure_overs",
                  "pressure_econ", "adj_pressure_dot_pct", "pressure_innings", "formats"]],
        use_container_width=True, hide_index=True
    )

with tab3:
    kind = st.radio("Player category", ["Batters", "Bowlers"], horizontal=True)
    if kind == "Batters":
        query = st.text_input("Search batter")
        view = bat_all.copy()
        if query:
            view = view[view.player.str.contains(query, case=False, na=False)]
    else:
        query = st.text_input("Search bowler")
        view = bowl_all.copy()
        if query:
            view = view[view.player.str.contains(query, case=False, na=False)]
    st.dataframe(view.sort_values("score", ascending=False), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("Ranking sensitivity checks")
    st.caption(
        "Top-10 overlap is measured against the corrected core model. "
        "Lower overlap means the list changes more under that assumption."
    )
    st.dataframe(sensitivity, use_container_width=True, hide_index=True)
    st.markdown("""
    **Interpretation**
    - The batter and bowler lists are not completely invariant to pressure thresholds, weights, or eligibility.
    - The exact Rank 1 changes under some pressure-definition tests.
    - Treat close score differences as uncertain; use the methodology report for assumptions and limitations.
    """)

with st.expander("Pressure definition and scoring"):
    st.markdown("""
    **Pressure flags**
    - Death: final five scheduled/revised overs.
    - Chase pressure: required run rate at least 10.
    - Collapse: at least 3 wickets lost in the first 30% (maximum six overs), or 5 wickets lost before 75% of the innings.
    - Clutch chase: no more than 30 balls and no more than 50 runs remaining.
    - Bowlers additionally face partnership pressure when the stand has reached 50 runs.

    **Batter score:** 25% adjusted pressure strike rate, 20% adjusted pressure average,
    20% strike-rate improvement over baseline, 15% consistency, 20% clutch strike rate.

    **Bowler score:** 30% adjusted pressure economy, 25% adjusted pressure average,
    20% adjusted dot-ball rate, 15% economy improvement over baseline, 10% pressure wicket rate.

    Percentiles are calculated separately within IPL and T20I. Core eligibility requires at least
    60 pressure balls and 8 pressure innings.
    """)
