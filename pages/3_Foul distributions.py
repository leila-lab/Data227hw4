import streamlit as st
from utils.io import load_data
from charts.charts import foul_distribution_dashboard

st.title("Foul Distributions")

st.write("""
This visualization examines disciplinary patterns across referees and teams.
The top chart compares referees based on the average number of fouls, yellow
cards, or red cards they issue per match across two seasons.

Selecting a referee highlights the teams most affected by that referee's
disciplinary style in the bottom chart.
""")

df = load_data()

chart = foul_distribution_dashboard(df)

st.altair_chart(chart, use_container_width=True)