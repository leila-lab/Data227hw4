import streamlit as st
from utils.io import load_data
from charts.charts import attacking_consistency_chart

st.title("Team Consistency")

df = load_data()

chart = attacking_consistency_chart(df)

st.altair_chart(chart, use_container_width=True)

import streamlit as st
from utils.io import load_data
from charts.charts import home_advantage_chart

st.title("Home Advantage")

df = load_data()

chart = home_advantage_chart(df)

st.altair_chart(chart, use_container_width=True)