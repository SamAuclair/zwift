"""
Global Metrics Dashboard - Page 1
Displays aggregate statistics across all training sessions
"""
import streamlit as st
from google.cloud import bigquery
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Metrics",
    page_icon="📊",
    layout="wide"
)

# Get BigQuery client from main app
if 'client' not in st.session_state:
    from pathlib import Path
    import os

    project_root = Path(__file__).parent.parent.parent
    credentials_path = project_root / "zwift-data-loader-key.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)
    st.session_state.client = bigquery.Client()

client = st.session_state.client

st.title("📊 Global Training Metrics")
st.markdown("Overview of all your training sessions")

# Year filter
st.sidebar.header("Filters")
year_filter = st.sidebar.selectbox(
    "Year",
    options=["All Years"],
    index=0
)

# Placeholder for metrics (to be implemented in next todo)
st.info("Global metrics will be displayed here. This includes training statistics, performance metrics, and cardio zone analysis.")

# Placeholder sections
st.markdown("### Training Statistics")
st.markdown("Total sessions, distance, and duration metrics will appear here.")

st.markdown("### Performance Metrics")
st.markdown("Heart rate, cadence, power, and speed statistics will appear here.")

st.markdown("### Cardio Zone Distribution")
st.markdown("Time spent in different cardio zones will be visualized here.")
