"""
Zwift Cycling Data Dashboard - Main Application
"""
import streamlit as st
from google.cloud import bigquery
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Zwift Training Dashboard",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme configuration
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
    }
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize BigQuery client
@st.cache_resource
def get_bigquery_client():
    """Initialize and cache BigQuery client with service account credentials"""
    # Look for credentials in project root
    project_root = Path(__file__).parent.parent
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

# Sidebar navigation
st.sidebar.title("🚴 Zwift Training Analytics")
st.sidebar.markdown("---")
st.sidebar.info(
    "Navigate between pages using the sidebar. "
    "This dashboard provides comprehensive insights into your Zwift training data."
)

# Main page content
st.title("Welcome to Zwift Training Dashboard")
st.markdown("""
This dashboard provides comprehensive analytics for your Zwift training sessions.

### Available Pages:
- **Global Metrics**: Overview of all training sessions with aggregate statistics
- **Training Session Details**: Deep dive into individual training sessions

Use the sidebar to navigate between pages.
""")

# Connection status
st.success("✅ Connected to BigQuery")
st.info(f"Project: {client.project}")
