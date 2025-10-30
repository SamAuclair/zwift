"""
Zwift Training Dashboard - Home Page
Redirects to Overview page
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Zwift Dashboard", page_icon="🚴", layout="wide", initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown(
    """
    <style>
    /* Hide the deploy button but keep sidebar toggle */
    button[kind="header"] {
        display: none;
    }
    .block-container {
        padding-top: 1rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Redirect message
st.title("🚴 Zwift Training Dashboard")
st.markdown(
    """
Welcome to my Zwift Training Dashboard!

Please use the navigation menu on the left to view:
- **Overview**: Global training statistics and performance metrics
- **Training Details**: Detailed analysis of individual training sessions
"""
)

st.info("👈 Select a page from the sidebar to get started")
