import streamlit as st
from utils.io import load_data
from charts.charts import league_position_chart

st.title("League Position Changes")

st.write("""
This visualization compares league rankings between the 2023–24 and
2024–25 seasons. Teams are ranked based on total wins.

Lines show how each team moved up or down in the standings between seasons.
""")

df = load_data()

chart = league_position_chart(df)

st.altair_chart(chart, use_container_width=True)