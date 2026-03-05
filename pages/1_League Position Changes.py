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
The chart indicates that rather than maintaining stability in attacking output over the course
of the season, it tends to vary over time with periods of relative high output followed by
periods of lower output. In the case illustrated above, it seems like the team faces a major
dip in attacking output in the middle of the season before resuming at a much higher level
in the later stages of the season.
""")

st.write("""
The above trends indicate how teams tend to have cycles rather than maintaining a constant
level in attacking output over time. Teams with smoother and steadier trends in rolling
averages tend to have better tactical consistency in comparison to teams with more volatile
trends in attacking output.
""")

st.write("""
The above visualization indicates how maintaining consistency in attacking output over
time—rather than focusing solely on peak scoring matches—plays a major role in ensuring
relative competitiveness over time in a full season of league matches.
""")