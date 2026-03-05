import streamlit as st

st.set_page_config(page_title="Premier League Narrative Visualization", layout="wide")

st.title("Premier League Narrative Visualization")

st.write("""
This project analyzes patterns in Premier League matches using data from
the 2023-24 and 2024-25 seasons.

The goal is to understand how team positions evolve over the season,
how consistent teams perform, and how disciplinary actions vary across matches.
""")

st.write("""
### Navigate the Story

**League Position Changes:**
We examine how team rankings change throughout the season.

**Team Consistency:**
We analyze how stable teams perform across matches.

**Foul Distributions:**
We explore disciplinary patterns and foul statistics.
""")