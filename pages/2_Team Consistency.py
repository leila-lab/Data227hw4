import streamlit as st
import altair as alt
import pandas as pd
from utils.io import load_data

st.title("Team Consistency")

st.write("""
This visualization examines how consistent teams are across the season by
tracking rolling averages of key attacking metrics over matchweeks.
""")

df = load_data()

# ------------------------------------------------
# Build long match-level dataset (home + away)
# ------------------------------------------------

home = df[[
    "Season","Date","HomeTeam","FTHG","HS","HST","HC"
]].copy()

home.columns = [
    "Season","Date","Team","Goals","Shots","ShotsOnTarget","Corners"
]

away = df[[
    "Season","Date","AwayTeam","FTAG","AS","AST","AC"
]].copy()

away.columns = [
    "Season","Date","Team","Goals","Shots","ShotsOnTarget","Corners"
]

long_df = pd.concat([home, away])

# ------------------------------------------------
# Sort properly so rolling averages work
# ------------------------------------------------

long_df = long_df.sort_values(["Season","Team","Date"])

long_df["Matchweek"] = (
    long_df.groupby(["Season","Team"]).cumcount() + 1
)

# ------------------------------------------------
# Reshape dataset for metric toggle
# ------------------------------------------------

metric_df = long_df.melt(
    id_vars=["Season","Team","Date","Matchweek"],
    value_vars=["Goals","Shots","ShotsOnTarget","Corners"],
    var_name="Metric",
    value_name="Value"
)

# ------------------------------------------------
# Compute 5-match rolling averages
# ------------------------------------------------

metric_df["RollingValue"] = (
    metric_df
    .groupby(["Season","Team","Metric"])["Value"]
    .transform(lambda x: x.rolling(5, min_periods=1).mean())
)

# ------------------------------------------------
# Streamlit controls
# ------------------------------------------------

team = st.selectbox(
    "Select Team",
    sorted(metric_df["Team"].unique())
)

season = st.radio(
    "Season",
    ["2023-24","2024-25"]
)

metric = st.radio(
    "Metric",
    ["Goals","Shots","ShotsOnTarget","Corners"]
)

filtered = metric_df[
    (metric_df["Team"] == team) &
    (metric_df["Season"] == season) &
    (metric_df["Metric"] == metric)
]

# ------------------------------------------------
# Build chart
# ------------------------------------------------

chart = (
    alt.Chart(filtered)
    .mark_line(size=3)
    .encode(
        x=alt.X("Matchweek:Q", title="Matchweek"),
        y=alt.Y("RollingValue:Q", title="5-Match Rolling Average"),
        tooltip=[
            "Team",
            "Season",
            "Matchweek",
            "Metric",
            "RollingValue"
        ]
    )
    .properties(
        width=750,
        height=450,
        title="Attacking Consistency Across Matchweeks"
    )
)

st.altair_chart(chart, use_container_width=True)

st.write("""
The chart highlights how attacking performance evolves throughout the season rather than
remaining constant. Some teams demonstrate sustained attacking pressure across many matchweeks,
while others experience significant swings in their offensive output.

Teams with smoother and more stable rolling averages tend to exhibit greater tactical
consistency, which may translate into more predictable match outcomes. In contrast, teams
with highly volatile attacking trends may struggle to maintain momentum across the season.
This suggests that sustained attacking performance—not just occasional strong matches—
plays an important role in overall team success.
""")