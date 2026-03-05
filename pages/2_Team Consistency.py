import streamlit as st
from utils.io import load_data
from charts.charts import (
    attacking_consistency_chart,
    home_advantage_chart
)

st.title("Team Consistency")

st.write("""
We analyze how consistent teams are offensively across the season
using rolling averages of attacking metrics.
""")

df = load_data()

# -----------------------
# Chart 1
# -----------------------

st.header("Attacking Consistency")

chart1 = attacking_consistency_chart(df)

st.altair_chart(chart1, use_container_width=True)


# -----------------------
# Chart 2
# -----------------------

st.header("Home Advantage")

season = st.radio(
    "Select Season",
    ["2023-24", "2024-25"]
)

chart2 = home_advantage_chart(df, season)

st.altair_chart(chart2, use_container_width=True)