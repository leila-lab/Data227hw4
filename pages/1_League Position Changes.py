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
Some of the teams experienced significant changes in their positions between
the two seasons. For example, the position of Liverpool has been enhanced
to ensure that they take the first position in the 2024-25 season, while
other teams, such as Manchester City, remain stable at the top of the
league table. On the other hand, there are teams such as Tottenham Hotspur
and West Ham United, which show significant changes in their positions, which
could be attributed to their performance in the following season.
""")

st.write("""
In conclusion, the visualization shows how the positions of the teams
change significantly between one season and another. This is attributed
to the fact that even small differences in the winning games can cause
significant changes in the final positions of the league, which is
characteristic of the Premier League. The changes show how dynamic the
performance of the teams is, where some of them move up while others move
down depending on their performance during the season.
""")