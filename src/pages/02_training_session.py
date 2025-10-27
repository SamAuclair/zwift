"""
Training Session Detail Dashboard - Page 2
Displays detailed metrics and time-series data for individual training sessions
"""
import streamlit as st
from google.cloud import bigquery
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Training Session Details",
    page_icon="📈",
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

st.title("📈 Training Session Details")
st.markdown("Deep dive into individual training session performance")

# Date picker filter
st.sidebar.header("Filters")
selected_date = st.sidebar.date_input(
    "Training Date",
    value=datetime.now().date()
)

# Placeholder for session metrics (to be implemented in next todo)
st.info("Session-specific metrics will be displayed here. This includes detailed performance statistics and time-series visualizations.")

# Placeholder sections
st.markdown("### Session Performance Metrics")
st.markdown("Heart rate, cadence, power, and speed statistics for the selected session will appear here.")

st.markdown("### Time-Series Analysis")
st.markdown("Interactive charts showing power and cadence over time will be visualized here.")
