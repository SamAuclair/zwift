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
    /* Global styles */
    .stApp {
        background-color: #1a1d23;
    }

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

    /* Title styling */
    h1 {
        font-weight: 300;
        letter-spacing: 2px;
        color: #ffffff;
    }

    div[data-testid="metric-container"] {
        background-color: #2a2d35;
        border: none;
        padding: 25px;
        border-radius: 8px;
        overflow-wrap: break-word;
        text-align: center;
        max-width: 300px;
        margin: 0 auto;
        position: relative;
    }

    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(45deg, #4a90e2, #50c878, #ffa500, #ff6b6b);
    }

    div[data-testid="stMetric"] {
        background-color: #2a2d35;
        border: none;
        padding: 25px;
        border-radius: 8px;
        text-align: center;
        max-width: 275px;
        margin: 0 auto;
        position: relative;
    }

    div[data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(45deg, #4a90e2, #50c878, #ffa500, #ff6b6b);
    }

    div[data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 300;
        color: #ffffff;
        text-align: center;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #8a8d93;
        font-weight: 400;
        text-align: center;
        padding-top: 0;
        margin-bottom: 8px;
    }
    label[data-testid="stMetricLabel"] {
        display: block;
        text-align: center;
    }
    label[data-testid="stMetricLabel"] div div p {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #8a8d93;
    }
    /* Keep section headers styled */
    h3 {
        text-align: left;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #8a8d93;
        font-weight: 400;
    }
    /* Position logo at the top of sidebar */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1rem;
    }
    section[data-testid="stSidebar"] [data-testid="stImage"] {
        margin-bottom: 2rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1a1d23;
        border-right: 1px solid #2a2d35;
    }

    /* Header with collapse/expand arrow */
    .stAppHeader, .stAppToolbar {
        background-color: #1a1d23;
    }

    [data-testid="stHeader"] {
        background-color: #1a1d23;
    }

    /* Reduce spacing between title and chart */
    div[data-testid="stPlotlyChart"] {
        margin-top: -1rem;
    }

    /* Responsive Design - Mobile devices */
    @media (max-width: 768px) {
        div[data-testid="stMetric"] {
            max-width: 100%;
            padding: 20px;
            margin-bottom: 1rem;
        }
        div[data-testid="metric-container"] {
            max-width: 100%;
            padding: 20px;
            margin-bottom: 1rem;
        }
        div[data-testid="stMetricValue"] {
            font-size: 28px;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 10px;
        }
        label[data-testid="stMetricLabel"] div div p {
            font-size: 10px;
        }
        h1 {
            font-size: 24px;
        }
        h3 {
            font-size: 12px;
        }
        .stMainBlockContainer {
            padding-top: 10px;
            padding-bottom: 10px;
        }
        div[data-testid="stPlotlyChart"] {
            margin-top: 0;
        }
        /* Make zone cards more readable on mobile */
        div[data-testid="column"] {
            padding-left: 0.25rem;
            padding-right: 0.25rem;
        }
    }

    /* Responsive Design - Tablets */
    @media (min-width: 769px) and (max-width: 1024px) {
        div[data-testid="stMetric"] {
            max-width: 240px;
        }
        div[data-testid="metric-container"] {
            max-width: 260px;
        }
        div[data-testid="stMetricValue"] {
            font-size: 28px;
        }
        label[data-testid="stMetricLabel"] div div p {
            font-size: 10px;
        }
        h1 {
            font-size: 28px;
        }
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


# Fetch session metrics from training table (already pre-aggregated)
@st.cache_data(ttl=600)
def get_session_metrics(selected_date):
    """Get detailed metrics for a specific training session"""
    query = f"""
    SELECT
        distance_km,
        duration,
        ROUND(max_heart_rate, 0) as max_heart_rate,
        ROUND(avg_heart_rate, 0) as avg_heart_rate,
        ROUND(max_cadence, 0) as max_cadence,
        ROUND(avg_cadence, 0) as avg_cadence,
        ROUND(max_power, 0) as max_power,
        ROUND(avg_power, 0) as avg_power,
        ROUND(max_speed_kmh, 1) as max_speed,
        ROUND(avg_speed_kmh, 1) as avg_speed
    FROM `zwift_data.training`
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


# Fetch cardio zone distribution for specific date
@st.cache_data(ttl=600)
def get_zone_distribution(selected_date):
    """Get time distribution across cardio zones for a specific date"""
    query = f"""
    SELECT
        'Zone 1' as zone_name,
        ROUND(percentage_time_zone_1, 4) as percentage
    FROM `zwift_data.zone`
    WHERE date = '{selected_date}'
    UNION ALL
    SELECT
        'Zone 2' as zone_name,
        ROUND(percentage_time_zone_2, 4) as percentage
    FROM `zwift_data.zone`
    WHERE date = '{selected_date}'
    UNION ALL
    SELECT
        'Zone 3' as zone_name,
        ROUND(percentage_time_zone_3, 4) as percentage
    FROM `zwift_data.zone`
    WHERE date = '{selected_date}'
    UNION ALL
    SELECT
        'Zone 4' as zone_name,
        ROUND(percentage_time_zone_4, 4) as percentage
    FROM `zwift_data.zone`
    WHERE date = '{selected_date}'
    UNION ALL
    SELECT
        'Zone 5' as zone_name,
        ROUND(percentage_time_zone_5, 4) as percentage
    FROM `zwift_data.zone`
    WHERE date = '{selected_date}'
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
        session_metrics = get_session_metrics(selected_date)
        timeseries_data = get_timeseries_data(selected_date)
        zone_distribution = get_zone_distribution(selected_date)

    if session_metrics.empty:
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
            margin=dict(t=20, b=10, l=40, r=20),
            font=dict(size=12),
            plot_bgcolor="#1a1d23",
            paper_bgcolor="#1a1d23",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "responsive": True,
            },
        )
    else:
        st.info("No time-series data available for this session.")

    # Cardio Zone Distribution Section

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
                    <div style="background-color: #2a2d35;
                                border-radius: 8px;
                                text-align: center;
                                color: #ffffff;
                                padding: 25px;
                                max-width: 275px;
                                margin: 0 auto 10px auto;
                                position: relative;">
                        <div style="content: '';
                                    position: absolute;
                                    top: 0;
                                    left: 0;
                                    right: 0;
                                    height: 2px;
                                    background: {zone_color};
                                    border-radius: 8px 8px 0 0;"></div>
                        <div style="font-size: 11px;
                                    text-transform: uppercase;
                                    letter-spacing: 2px;
                                    color: #8a8d93;
                                    font-weight: 400;
                                    margin-bottom: 8px;">{zone['zone_name']}</div>
                        <div style="font-size: 32px;
                                    font-weight: 300;
                                    color: #ffffff;">{zone['percentage']* 100:.1f}%</div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
        st.markdown("---")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(label="Distance", value=f"{session_metrics['distance_km'].iloc[0]:.1f} km")

        with col2:
            # Convert seconds to HH:MM:SS
            duration_seconds = session_metrics["duration"].iloc[0]
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
            st.metric(
                label="Avg. Cadence 🔄", value=f"{int(session_metrics['avg_cadence'].iloc[0])} rpm"
            )
            st.metric(label="Max Cadence 🔄", value=f"{int(session_metrics['max_cadence'].iloc[0])} rpm")
    else:
        st.info("No cardio zone data available for the selected date.")

    # Add some bottom spacing
    st.markdown("<br>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading session details: {e}")
    st.info("Please ensure the BigQuery tables exist and contain data for the selected date.")
