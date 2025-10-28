"""
Global Metrics Dashboard - Page 1
Displays aggregate statistics across all training sessions
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from google.cloud import bigquery

st.set_page_config(page_title="Global Metrics", page_icon="📊", layout="wide")

# Get BigQuery client from main app
if "client" not in st.session_state:
    import os
    from pathlib import Path

    project_root = Path(__file__).parent.parent.parent
    credentials_path = project_root / "zwift-data-loader-key.json"
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)
    st.session_state.client = bigquery.Client()

client = st.session_state.client

st.title("📊 Global Training Metrics")
st.markdown("Overview of all your training sessions")


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

    # Training Statistics Section
    st.markdown("### 📈 Training Statistics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Training Sessions", value=f"{int(training_metrics['total_sessions'].iloc[0]):,}"
        )

    with col2:
        st.metric(
            label="Total Distance", value=f"{training_metrics['total_distance_km'].iloc[0]:,.2f} km"
        )

    with col3:
        st.metric(
            label="Avg Distance per Session",
            value=f"{training_metrics['avg_distance_km'].iloc[0]:.2f} km",
        )

    with col4:
        # Convert seconds to HH:MM:SS
        avg_seconds = training_metrics["avg_duration_seconds"].iloc[0]
        hours = int(avg_seconds // 3600)
        minutes = int((avg_seconds % 3600) // 60)
        seconds = int(avg_seconds % 60)
        st.metric(label="Avg Duration per Session", value=f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    st.markdown("---")

    # Performance Metrics Section
    st.markdown("### 💪 Performance Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("#### ❤️ Heart Rate")
        st.metric(label="Max", value=f"{int(performance_metrics['max_heart_rate'].iloc[0])} bpm")
        st.metric(label="Average", value=f"{int(performance_metrics['avg_heart_rate'].iloc[0])} bpm")

    with col2:
        st.markdown("#### ⚡ Power")
        st.metric(label="Max", value=f"{int(performance_metrics['max_power'].iloc[0])} W")
        st.metric(label="Average", value=f"{int(performance_metrics['avg_power'].iloc[0])} W")

    with col3:
        st.markdown("#### 🔄 Cadence")
        st.metric(label="Max", value=f"{int(performance_metrics['max_cadence'].iloc[0])} rpm")
        st.metric(label="Average", value=f"{int(performance_metrics['avg_cadence'].iloc[0])} rpm")

    with col4:
        st.markdown("#### 🚴 Speed")
        st.metric(label="Max", value=f"{performance_metrics['max_speed'].iloc[0]:.1f} km/h")
        st.metric(label="Average", value=f"{performance_metrics['avg_speed'].iloc[0]:.1f} km/h")

    st.markdown("---")

    # Cardio Zone Distribution Section
    st.markdown("### 🎯 Cardio Zone Distribution")

    if not zone_distribution.empty:
        # Create bar chart with custom colors
        zone_colors = ['#92FC29', '#ADCE2D', '#C9A130', '#E47334', '#FF4537']
        fig = px.bar(
            zone_distribution,
            x="zone_name",
            y="percentage",
            labels={"zone_name": "Zone", "percentage": "Time Percentage (%)"},
            title="Time Distribution Across Cardio Zones",
            color="zone_name",
            color_discrete_sequence=zone_colors,
        )
        fig.update_layout(
            xaxis_title="Cardio Zone", yaxis_title="Percentage of Time (%)", showlegend=False, height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Display data table
        st.markdown("#### Zone Details")
        zone_display = zone_distribution.copy()
        zone_display.columns = ["Zone", "Time (%)"]
        st.dataframe(zone_display, use_container_width=True, hide_index=True)
    else:
        st.info("No cardio zone data available for the selected period.")

except Exception as e:
    st.error(f"Error loading metrics: {e}")
    st.info("Please ensure the BigQuery tables exist and contain data.")
