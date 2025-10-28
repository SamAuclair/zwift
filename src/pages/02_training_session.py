"""
Training Session Detail Dashboard - Page 2
Displays detailed metrics and time-series data for individual training sessions
"""

from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from google.cloud import bigquery

st.set_page_config(page_title="Training Session Details", page_icon="📈", layout="wide")

# Get BigQuery client from main app
if "client" not in st.session_state:
    import os
    from pathlib import Path

    project_root = Path(__file__).parent.parent.parent
    credentials_path = project_root / "zwift-data-loader-key.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)
    st.session_state.client = bigquery.Client()

client = st.session_state.client

st.title("📈 Training Session Details")


# Fetch available training dates
@st.cache_data(ttl=600)
def get_available_dates():
    """Get list of dates with training data"""
    query = """
    SELECT DISTINCT date
    FROM `zwift_data.training`
    ORDER BY date DESC
    """
    df = client.query(query).to_dataframe()
    return df["date"].tolist()


# Fetch session metrics
@st.cache_data(ttl=600)
def get_session_metrics(selected_date):
    """Get detailed metrics for a specific training session"""
    query = f"""
    SELECT
        ROUND(MAX(heart_rate), 0) as max_heart_rate,
        ROUND(AVG(heart_rate), 0) as avg_heart_rate,
        ROUND(MAX(cadence), 0) as max_cadence,
        ROUND(AVG(cadence), 0) as avg_cadence,
        ROUND(MAX(power), 0) as max_power,
        ROUND(AVG(power), 0) as avg_power,
        ROUND(MAX(speed_kmh), 1) as max_speed,
        ROUND(AVG(speed_kmh), 1) as avg_speed
    FROM `zwift_data.augmented_data`
    WHERE date = '{selected_date}'
    """
    return client.query(query).to_dataframe()


# Fetch time-series data
@st.cache_data(ttl=600)
def get_timeseries_data(selected_date):
    """Get time-series data for power and cadence visualization"""
    query = f"""
    SELECT
        local_timestamp,
        time,
        power,
        cadence,
        heart_rate,
        speed_kmh
    FROM `zwift_data.augmented_data`
    WHERE date = '{selected_date}'
    ORDER BY local_timestamp
    """
    return client.query(query).to_dataframe()


# Fetch training session info
@st.cache_data(ttl=600)
def get_session_info(selected_date):
    """Get basic session information from training table"""
    query = f"""
    SELECT
        distance_km,
        duration,
        avg_speed_kmh,
        avg_cadence,
        avg_power,
        avg_heart_rate
    FROM `zwift_data.training`
    WHERE date = '{selected_date}'
    """
    return client.query(query).to_dataframe()


# Date picker filter
st.sidebar.header("Filters")

try:
    available_dates = get_available_dates()

    if not available_dates:
        st.error("No training sessions found in the database.")
        st.stop()

    # Format dates for display and create selectbox
    date_options = [d.strftime("%Y-%m-%d") for d in available_dates]

    selected_date_str = st.sidebar.selectbox(
        "Training Date", options=date_options, index=0  # Default to latest (first in list)
    )

    # Convert selected string back to date object
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()

    # Fetch data for selected date
    session_info = get_session_info(selected_date)
    session_metrics = get_session_metrics(selected_date)
    timeseries_data = get_timeseries_data(selected_date)

    if session_info.empty or session_metrics.empty:
        st.error(f"No data available for {selected_date}")
        st.stop()

    # Display session summary
    st.markdown(f"### 📅 Session Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Date", value=f"{selected_date}")

    with col2:
        # Convert seconds to HH:MM:SS
        duration_seconds = session_info["duration"].iloc[0]
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        st.metric(label="Duration", value=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    with col3:
        st.metric(label="Distance", value=f"{session_info['distance_km'].iloc[0]:.2f} km")

    # Performance Metrics Section
    st.markdown("### 💪 Session Performance Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("#### ❤️ Heart Rate")
        st.metric(label="Max", value=f"{int(session_metrics['max_heart_rate'].iloc[0])} bpm")
        st.metric(label="Average", value=f"{int(session_metrics['avg_heart_rate'].iloc[0])} bpm")

    with col2:
        st.markdown("#### ⚡ Power")
        st.metric(label="Max", value=f"{int(session_metrics['max_power'].iloc[0])} W")
        st.metric(label="Average", value=f"{int(session_metrics['avg_power'].iloc[0])} W")

    with col3:
        st.markdown("#### 🔄 Cadence")
        st.metric(label="Max", value=f"{int(session_metrics['max_cadence'].iloc[0])} rpm")
        st.metric(label="Average", value=f"{int(session_metrics['avg_cadence'].iloc[0])} rpm")

    with col4:
        st.markdown("#### 🚴 Speed")
        st.metric(label="Max", value=f"{session_metrics['max_speed'].iloc[0]:.1f} km/h")
        st.metric(label="Average", value=f"{session_metrics['avg_speed'].iloc[0]:.1f} km/h")

    # st.markdown("---")

    # Time-Series Analysis Section
    st.markdown("### 📊 Time-Series Analysis")

    if not timeseries_data.empty:
        # Create chart for Power and Heart Rate
        fig = go.Figure()

        # Add Power trace
        fig.add_trace(
            go.Scatter(
                x=timeseries_data["local_timestamp"],
                y=timeseries_data["power"],
                name="Power",
                line=dict(color="#FF4537", width=2),
            )
        )

        # Add Heart Rate trace
        fig.add_trace(
            go.Scatter(
                x=timeseries_data["local_timestamp"],
                y=timeseries_data["heart_rate"],
                name="Heart Rate",
                line=dict(color="#E47334", width=2),
            )
        )

        # Configure layout with single y-axis
        fig.update_layout(
            title="Power and Heart Rate Over Time",
            xaxis=dict(title="Time"),
            yaxis=dict(title="Value"),
            hovermode="x unified",
            height=500,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )

        st.plotly_chart(fig, use_container_width=True)

        # Additional charts
        col1, col2 = st.columns(2)

        with col1:
            # Heart rate over time
            fig_hr = px.line(
                timeseries_data,
                x="local_timestamp",
                y="heart_rate",
                title="Heart Rate Over Time",
                labels={"local_timestamp": "Time", "heart_rate": "Heart Rate (bpm)"},
            )
            fig_hr.update_traces(line_color="#E47334")
            fig_hr.update_layout(height=400)
            st.plotly_chart(fig_hr, use_container_width=True)

        with col2:
            # Speed over time
            fig_speed = px.line(
                timeseries_data,
                x="local_timestamp",
                y="speed_kmh",
                title="Speed Over Time",
                labels={"local_timestamp": "Time", "speed_kmh": "Speed (km/h)"},
            )
            fig_speed.update_traces(line_color="#ADCE2D")
            fig_speed.update_layout(height=400)
            st.plotly_chart(fig_speed, use_container_width=True)
    else:
        st.info("No time-series data available for this session.")

except Exception as e:
    st.error(f"Error loading session details: {e}")
    st.info("Please ensure the BigQuery tables exist and contain data for the selected date.")
