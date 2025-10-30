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

st.set_page_config(
    page_title="Zwift Dashboard", page_icon="🚴", layout="wide", initial_sidebar_state="expanded"
)

# Custom CSS for card styling
st.markdown(
    """
    <style>
    /* Hide the deploy button but keep sidebar toggle */
    button[kind="header"] {
        display: none;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stMainBlockContainer {
        padding-top: 20px;
        padding-bottom: 20px;
    }

    div[data-testid="metric-container"] {
        background-color: #262626;
        border: 2px solid #505050;
        padding: 5%;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.6);
        overflow-wrap: break-word;
        text-align: center;
        max-width: 300px;
        margin: 0 auto;
    }
    div[data-testid="stMetric"] {
        background-color: #262626;
        border: 2px solid #505050;
        padding: 2%;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.6);
        text-align: center;
        max-width: 275px;
        margin: 0 auto;
    }
    div[data-testid="stMetricValue"] {
        font-size: 36px;
        font-weight: bold;
        color: #FFFFFF;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 18px;
        color: #BBBBBB;
        font-weight: 500;
        text-align: center;
        padding-top: 0;
    }
    label[data-testid="stMetricLabel"] {
        display: block;
        text-align: center;
    }
    label[data-testid="stMetricLabel"] div div p {
        font-size: 18px;
    }
    /* Keep section headers left-aligned */
    h3 {
        text-align: left;
    }
    /* Position logo at the top of sidebar */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    section[data-testid="stSidebar"] [data-testid="stImage"] {
        margin-bottom: 2rem;
    }
    /* Reduce spacing between title and chart */
    div[data-testid="stPlotlyChart"] {
        margin-top: -1rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Get BigQuery client from main app
if "client" not in st.session_state:
    import os
    from pathlib import Path

    project_root = Path(__file__).parent.parent.parent
    credentials_path = project_root / "zwift-data-loader-key.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)
    st.session_state.client = bigquery.Client()

client = st.session_state.client

# Add Zwift logo to sidebar
from pathlib import Path

logo_path = Path(__file__).parent.parent / "assets" / "zwift_logo.png"
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)


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


# Fetch cardio zone distribution for specific date
@st.cache_data(ttl=600)
def get_zone_distribution(selected_date):
    """Get time distribution across cardio zones for a specific date"""
    query = f"""
    WITH zone_totals AS (
        SELECT
            time_zone_1 as total_zone_1,
            time_zone_2 as total_zone_2,
            time_zone_3 as total_zone_3,
            time_zone_4 as total_zone_4,
            time_zone_5 as total_zone_5
        FROM `zwift_data.zone`
        WHERE date = '{selected_date}'
    ),
    total_time AS (
        SELECT
            total_zone_1 + total_zone_2 + total_zone_3 + total_zone_4 + total_zone_5 as total
        FROM zone_totals
    )
    SELECT 'Zone 1' as zone_name, ROUND((zone_totals.total_zone_1 / total_time.total) * 100, 2) as percentage
    FROM zone_totals, total_time
    UNION ALL
    SELECT 'Zone 2' as zone_name, ROUND((zone_totals.total_zone_2 / total_time.total) * 100, 2) as percentage
    FROM zone_totals, total_time
    UNION ALL
    SELECT 'Zone 3' as zone_name, ROUND((zone_totals.total_zone_3 / total_time.total) * 100, 2) as percentage
    FROM zone_totals, total_time
    UNION ALL
    SELECT 'Zone 4' as zone_name, ROUND((zone_totals.total_zone_4 / total_time.total) * 100, 2) as percentage
    FROM zone_totals, total_time
    UNION ALL
    SELECT 'Zone 5' as zone_name, ROUND((zone_totals.total_zone_5 / total_time.total) * 100, 2) as percentage
    FROM zone_totals, total_time
    ORDER BY zone_name
    """
    return client.query(query).to_dataframe()


# Date picker filter
st.sidebar.header("Filters")

try:
    with st.spinner("Loading available training dates..."):
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

    # Display title with selected date
    st.title(f"Training Details ({selected_date_str})")

    # Fetch data for selected date
    with st.spinner("Loading session details..."):
        session_info = get_session_info(selected_date)
        session_metrics = get_session_metrics(selected_date)
        timeseries_data = get_timeseries_data(selected_date)
        zone_distribution = get_zone_distribution(selected_date)

    if session_info.empty or session_metrics.empty:
        st.error(f"No data available for {selected_date}")
        st.stop()

    if not timeseries_data.empty:
        # Create chart for Power and Heart Rate
        fig = go.Figure()

        # Add Power trace (blue)
        fig.add_trace(
            go.Scatter(
                x=timeseries_data["local_timestamp"],
                y=timeseries_data["power"],
                name="Power",
                line=dict(color="#1f77b4", width=2),
                hovertemplate="Power: %{y:.0f} W<extra></extra>",
            )
        )

        # Add Heart Rate trace
        fig.add_trace(
            go.Scatter(
                x=timeseries_data["local_timestamp"],
                y=timeseries_data["heart_rate"],
                name="Heart Rate",
                line=dict(color="#E47334", width=2),
                hovertemplate="Heart Rate: %{y:.0f} bpm<extra></extra>",
            )
        )

        # Configure layout with single y-axis (no title)
        fig.update_layout(
            yaxis=dict(title=""),
            hovermode="x unified",
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(t=20, b=10),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No time-series data available for this session.")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Distance", value=f"{session_info['distance_km'].iloc[0]:.1f} km")

    with col2:
        # Convert seconds to HH:MM:SS
        duration_seconds = session_info["duration"].iloc[0]
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        st.metric(label="Duration", value=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Avg. Heart Rate ❤️", value=f"{int(session_metrics['avg_heart_rate'].iloc[0])} bpm"
        )
        st.metric(
            label="Max Heart Rate ❤️", value=f"{int(session_metrics['max_heart_rate'].iloc[0])} bpm"
        )

    with col2:
        st.metric(label="Avg. Power ⚡", value=f"{int(session_metrics['avg_power'].iloc[0])} W")
        st.metric(label="Max Power ⚡", value=f"{int(session_metrics['max_power'].iloc[0])} W")

    with col3:
        st.metric(label="Avg. Speed 🚴", value=f"{session_metrics['avg_speed'].iloc[0]:.1f} km/h")
        st.metric(label="Max Speed 🚴", value=f"{session_metrics['max_speed'].iloc[0]:.1f} km/h")

    with col4:
        st.metric(label="Avg. Cadence 🔄", value=f"{int(session_metrics['avg_cadence'].iloc[0])} rpm")
        st.metric(label="Max Cadence 🔄", value=f"{int(session_metrics['max_cadence'].iloc[0])} rpm")

    # Cardio Zone Distribution Section
    st.markdown("---")
    st.markdown("### Time Spent in Cardio Zones")

    if not zone_distribution.empty:
        # Create 5 individual zone cards with color-coded backgrounds
        zone_colors = ["#92FC29", "#ADCE2D", "#C9A130", "#E47334", "#FF4537"]
        zone_data = zone_distribution.to_dict("records")

        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        for idx, (col, zone) in enumerate(zip(cols, zone_data)):
            with col:
                zone_color = zone_colors[idx]
                st.markdown(
                    f"""
                    <div style="background-color: {zone_color};
                                border-radius: 10px;
                                text-align: center;
                                color: #000000;
                                font-weight: bold;
                                max-height: 100px;
                                display: flex;
                                flex-direction: column;
                                justify-content: center;">
                        <div style="font-size: 24px; margin-top: 5px;">{zone['zone_name']}</div>
                        <div style="font-size: 32px; margin-bottom: 5px;">{zone['percentage']:.1f}%</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("No cardio zone data available for the selected date.")

    # Add some bottom spacing
    st.markdown("<br>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading session details: {e}")
    st.info("Please ensure the BigQuery tables exist and contain data for the selected date.")
