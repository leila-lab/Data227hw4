import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    s2324 = pd.read_csv("data/season-2324.csv")
    s2425 = pd.read_csv("data/season-2425.csv")

    s2324["Season"] = "2023-24"
    s2425["Season"] = "2024-25"

    df = pd.concat([s2324, s2425], ignore_index=True)

    return df