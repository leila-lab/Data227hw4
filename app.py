import streamlit as st

st.set_page_config(
    page_title="Premier League Performance Story",
    layout="wide"
)

st.title("Premier League Performance: A Narrative Visualization")

st.write("""
This project presents a narrative visualization analyzing the performance
of English Premier League teams.

Using interactive charts built with Altair and deployed with Streamlit,
we explore patterns in team performance and match outcomes.
""")

st.write("""
### How to Navigate This Story

**Central Narrative**
We analyze key patterns in team performance and match statistics.

**Exploration**
Readers can interactively explore relationships between different metrics.

**Methodology**
We describe the dataset and discuss limitations of the analysis.
""")