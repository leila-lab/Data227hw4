import streamlit as st
import altair as alt
import pandas as pd
from utils.io import load_data

st.title("Team Consistency")

df = load_data()

# -----------------------
# Build long dataset
# -----------------------

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

long_df = long_df.sort_values(["Season","Team","Date"])

long_df["Matchweek"] = (
    long_df.groupby(["Season","Team"]).cumcount() + 1
)

metric_df = long_df.melt(
    id_vars=["Season","Team","Date","Matchweek"],
    value_vars=["Goals","Shots","ShotsOnTarget","Corners"],
    var_name="Metric",
    value_name="Value"
)

metric_df["RollingValue"] = (
    metric_df
    .groupby(["Season","Team","Metric"])["Value"]
    .transform(lambda x: x.rolling(5, min_periods=1).mean())
)

# -----------------------
# Streamlit controls
# -----------------------

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

# -----------------------
# Chart
# -----------------------

chart = (
    alt.Chart(filtered)
    .mark_line(size=3)
    .encode(
        x=alt.X("Matchweek:Q", title="Matchweek"),
        y=alt.Y("RollingValue:Q", title="5-Match Rolling Average"),
        tooltip=["Team","Season","Matchweek","Metric","RollingValue"]
    )
    .properties(
        width=750,
        height=450,
        title="Attacking Consistency Across Matchweeks"
    )
)

import streamlit as st
from utils.io import load_data
from charts.charts import home_advantage_dashboard

st.title("Home Advantage")

df = load_data()

season = st.radio(
    "Select Season",
    ["2023-24","2024-25"]
)

chart = home_advantage_dashboard(df, season)

st.altair_chart(chart, use_container_width=True)