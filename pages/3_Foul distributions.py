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
Together, these visualizations highlight meaningful differences in how referees manage
disciplinary actions during matches. The top chart shows that referees vary noticeably
in the average number of fouls, yellow cards, and red cards they issue per match across
seasons. Some referees consistently produce higher disciplinary totals, suggesting a
stricter officiating style, while others appear more lenient.

The bottom chart reveals how these refereeing tendencies translate to the team level.
When a specific referee is selected, we can see which teams tend to accumulate the most
cards or fouls in matches they officiate. While some variation may reflect team playing
styles, the patterns also suggest that referee decisions can meaningfully influence the
disciplinary intensity of matches.

Overall, these findings illustrate that disciplinary outcomes in football are shaped not
only by team behavior but also by the referees overseeing the match, highlighting an
important contextual factor in understanding match dynamics.
""")