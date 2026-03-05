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

st.write("""
The visualization reveals that while a few teams maintained relatively stable positions,
many experienced noticeable shifts in ranking between seasons. For example, Liverpool
improved their position to finish first in 2024–25, while teams such as Tottenham and
West Ham dropped significantly in the standings.

These movements suggest that league performance can fluctuate substantially from year
to year, even for established teams. Small differences in wins can translate into large
changes in final league position, highlighting the competitive nature of the Premier
League and the importance of consistent performance across the season.
""")