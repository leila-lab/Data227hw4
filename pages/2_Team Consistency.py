import streamlit as st
from utils.io import load_data
from charts.charts import team_consistency_chart

st.title("Team Consistency")

df = load_data()

chart = team_consistency_chart(df)

st.altair_chart(chart, use_container_width=True)

import streamlit as st
from utils.io import load_data
from charts.charts import home_advantage_dashboard

st.title("Home Advantage Across Teams")

df = load_data()

chart = home_advantage_dashboard(df)

st.altair_chart(chart, use_container_width=True)