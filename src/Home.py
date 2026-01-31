"""
Zwift Training Dashboard - Landing Page
Welcome page explaining the project architecture and dashboard navigation
"""

from pathlib import Path

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Zwift Dashboard - Home",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
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

    /* Section headers */
    h2 {
        font-size: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #8a8d93;
        font-weight: 400;
        margin-top: 2rem;
    }

    h3 {
        text-align: left;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #8a8d93;
        font-weight: 400;
    }

    /* Content text */
    p, li {
        color: #ffffff;
        font-size: 16px;
        line-height: 1.8;
    }

    /* Markdown container text */
    #stMarkdownContainer p,
    #stMarkdownContainer ul,
    .st-emotion-cache-467cry p,
    .st-emotion-cache-467cry ul {
        font-size: 1.25rem !important;
    }

    /* Info box styling */
    .info-box {
        background-color: #2a2d35;
        border-left: 4px solid #f36622;
        padding: 20px;
        border-radius: 8px;
        margin: 20px 0;
    }

    .info-box,
    .info-box * {
        font-size: 1.25rem !important;
    }

    /* Pipeline box styling */
    .pipeline-box {
        background-color: #2a2d35;
        border: 2px solid #f36622;
        padding: 25px;
        border-radius: 8px;
        margin: 20px 0;
        text-align: center;
    }

    .pipeline-box,
    .pipeline-box * {
        font-size: 1.25rem !important;
    }

    .pipeline-step {
        display: inline-block;
        margin: 0 10px;
        color: #f36622;
        font-weight: 500;
    }

    .pipeline-arrow {
        display: inline-block;
        margin: 0 5px;
        color: #8a8d93;
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

# Add Zwift logo to sidebar
logo_path = Path(__file__).parent / "assets" / "zwift_logo.png"
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)

# Main content
st.title("🚴 Zwift Dashboard")

st.markdown(
    """
Zwift is a indoor cycling platform that allows you to ride with cyclists from around the world.
At the end of each ride, a ".FIT" file that contain details about the training session is generated.
I have built an ELT data pipeline that parses the .FIT file, load it into Big Query, 
transform the data with DBT and visualize it with the Streamlit Python library.
This project demonstrates end-to-end data engineering and visualization capabilities. 
For more details, [see the project on github](https://github.com/SamAuclair/zwift).
"""
)

st.markdown(
    """
    <div class="pipeline-box">
        <span class="pipeline-step">Zwift (.FIT files)</span>
        <span class="pipeline-arrow">→</span>
        <span class="pipeline-step">Airflow (Orchestrate)</span>
        <span class="pipeline-arrow">→</span>
        <span class="pipeline-step">Python (Extract)</span>
        <span class="pipeline-arrow">→</span>
        <span class="pipeline-step">BigQuery (Load)</span>
        <span class="pipeline-arrow">→</span>
        <span class="pipeline-step">DBT (Transform)</span>
        <span class="pipeline-arrow">→</span>
        <span class="pipeline-step">Streamlit Dashboard</span>
    </div>
""",
    unsafe_allow_html=True,
)

# Getting Started
st.markdown("### 🚀 Getting Started")

st.markdown(
    """
Navigate using the left sidebar to explore different aspects of my training data:
- **Global Statistics**: Start with the **Global Statistics** page for a high-level summary.
- **Training Details**: Use the **Training Details** page to analyze specific rides.
"""
)

st.markdown(
    """
    <div class="info-box">
        💡 <strong>Tip:</strong> Both pages of this dashboard can be filtered from the left sidebar.    
    </div>
""",
    unsafe_allow_html=True,
)

# This dashboard automatically refreshes data from BigQuery every 10 minutes.
#         New training sessions will appear shortly after being uploaded to the data warehouse.
