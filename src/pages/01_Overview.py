"""
Zwift Training Overview Dashboard - Main Page
Displays aggregate statistics across all training sessions
"""

import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from google.cloud import bigquery

# Page configuration
st.set_page_config(
    page_title="Zwift Dashboard",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded",
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
        max-width: 250px;
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
    </style>
""",
    unsafe_allow_html=True,
)


# Initialize BigQuery client
@st.cache_resource
def get_bigquery_client():
    """Initialize and cache BigQuery client with service account credentials"""
    # Look for credentials in project root
    project_root = Path(__file__).parent.parent.parent
    credentials_path = project_root / "zwift-data-loader-key.json"

    if not credentials_path.exists():
        st.error(f"BigQuery credentials not found at: {credentials_path}")
        st.stop()

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)

    try:
        client = bigquery.Client()
        return client
    except Exception as e:
        st.error(f"Failed to initialize BigQuery client: {e}")
        st.stop()


# Initialize client
client = get_bigquery_client()

# Add Zwift logo to sidebar
logo_path = Path(__file__).parent.parent / "assets" / "zwift_logo.png"
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)


# Fetch available years from data
@st.cache_data(ttl=600)
def get_available_years():
    """Get list of years with training data"""
    query = """
    SELECT DISTINCT EXTRACT(YEAR FROM date) as year
    FROM `zwift_data.training`
    ORDER BY year DESC
    """
    df = client.query(query).to_dataframe()
    return ["All Years"] + [str(int(year)) for year in df["year"].tolist()]


# Year filter
st.sidebar.header("Filters")
available_years = get_available_years()
year_filter = st.sidebar.selectbox("Year", options=available_years, index=0)

# Display title with selected year
st.title(f"Zwift Training Statistics for: {year_filter}")

# Build year filter condition for queries
year_condition = ""
if year_filter != "All Years":
    year_condition = f"WHERE EXTRACT(YEAR FROM date) = {year_filter}"


# Fetch global training metrics
@st.cache_data(ttl=600)
def get_training_metrics(year_cond):
    """Get global training statistics"""
    query = f"""
    WITH session_metrics AS (
        SELECT
            date,
            distance_km,
            duration
        FROM `zwift_data.training`
        {year_cond}
    )
    SELECT
        COUNT(DISTINCT date) as total_sessions,
        ROUND(SUM(distance_km), 2) as total_distance_km,
        ROUND(AVG(distance_km), 2) as avg_distance_km,
        AVG(duration) as avg_duration_seconds
    FROM session_metrics
    """
    return client.query(query).to_dataframe()


# Fetch performance metrics
@st.cache_data(ttl=600)
def get_performance_metrics(year_cond):
    """Get performance statistics from augmented_data"""
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
    {year_cond}
    """
    return client.query(query).to_dataframe()


# Fetch cardio zone distribution
@st.cache_data(ttl=600)
def get_zone_distribution(year_cond):
    """Get time distribution across cardio zones"""
    query = f"""
    WITH zone_totals AS (
        SELECT
            SUM(time_zone_1) as total_zone_1,
            SUM(time_zone_2) as total_zone_2,
            SUM(time_zone_3) as total_zone_3,
            SUM(time_zone_4) as total_zone_4,
            SUM(time_zone_5) as total_zone_5
        FROM `zwift_data.zone`
        {year_cond}
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


# Fetch data
try:
    training_metrics = get_training_metrics(year_condition)
    performance_metrics = get_performance_metrics(year_condition)
    zone_distribution = get_zone_distribution(year_condition)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Training Sessions", value=f"{int(training_metrics['total_sessions'].iloc[0]):,}"
        )

    with col2:
        st.metric(
            label="Total Distance", value=f"{training_metrics['total_distance_km'].iloc[0]:,.1f} km"
        )

    with col3:
        st.metric(
            label="Avg. Distance per Session",
            value=f"{training_metrics['avg_distance_km'].iloc[0]:.1f} km",
        )

    with col4:
        # Convert seconds to HH:MM:SS
        avg_seconds = training_metrics["avg_duration_seconds"].iloc[0]
        hours = int(avg_seconds // 3600)
        minutes = int((avg_seconds % 3600) // 60)
        seconds = int(avg_seconds % 60)
        st.metric(label="Avg. Duration per Session", value=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Avg. Heart Rate ❤️",
            value=f"{int(performance_metrics['avg_heart_rate'].iloc[0])} bpm",
        )
        st.metric(
            label="Max Hearth Rate ❤️", value=f"{int(performance_metrics['max_heart_rate'].iloc[0])} bpm"
        )

    with col2:
        st.metric(label="Avg. Power⚡", value=f"{int(performance_metrics['avg_power'].iloc[0])} W")
        st.metric(label="Max Power ⚡", value=f"{int(performance_metrics['max_power'].iloc[0])} W")

    with col3:
        st.metric(label="Avg. Speed 🚴", value=f"{performance_metrics['avg_speed'].iloc[0]:.1f} km/h")
        st.metric(label="Max Speed 🚴", value=f"{performance_metrics['max_speed'].iloc[0]:.1f} km/h")

    with col4:
        st.metric(
            label="Avg. Cadence 🔄", value=f"{int(performance_metrics['avg_cadence'].iloc[0])} rpm"
        )
        st.metric(label="Max Cadence 🔄", value=f"{int(performance_metrics['max_cadence'].iloc[0])} rpm")

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
        st.info("No cardio zone data available for the selected period.")

except Exception as e:
    st.error(f"Error loading metrics: {e}")
    st.info("Please ensure the BigQuery tables exist and contain data.")
