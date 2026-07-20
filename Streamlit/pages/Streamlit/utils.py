import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_data():
    # Project Root
    root = Path(__file__).parent.parent

    # Dataset Path
    data_path = root / "Data" / "indian_tech_jobs_cleaned.csv"

    df = pd.read_csv(data_path)

    return df