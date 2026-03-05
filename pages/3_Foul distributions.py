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

st.write("""
The visualizations also reveal some of the significant differences that exist 
in the refereeing of matches in the EPL league. The first visualization indicates
that referees in the league have different tendencies when it comes 
to the average number of fouls, yellow cards, and red cards in the matches
that they officiate in different seasons of the league. The second visualization
indicates that referees also have different impacts on the teams that they 
officiate in the league matches. The visualization indicates that when 
a referee is chosen to officiate in the matches of the league, it 
reveals the teams that receive the most fouls and cards in the matches that 
the referee officiates in the league.

The results of the analysis indicate that the disciplinary actions in
the matches of the EPL league are not solely determined by the teams that 
participate in the matches. The analysis also indicates
that the refereeing style of the referees has a 
significant impact on the matches that the referees officiate in the EPL league.
For example, the refereeing style of the referee S. Allison in the 2024-25 
season was significantly different from the refereeing 
style of the same referee in the 2023-24 season. The 
refereeing style of the same referee in the 2024-25 season of the 
league indicates that she issued many more fouls and yellow cards
in the 2024-25 than in 2023-24.
""")