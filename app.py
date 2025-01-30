import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Tenzin Quantum | AI Trading",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for Tesla-inspired design
st.markdown("""
<style>
    /* Import Tesla-inspired font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Global theme */
    :root {
        --background-color: #000000;
        --text-color: #FFFFFF;
        --accent-color: #E31937;  /* Tesla Red */
        --success-color: #00FF00;
        --warning-color: #FFB800;
        --card-bg: #111111;
        --hover-color: #222222;
    }
    
    /* Main background */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Roboto', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Roboto', sans-serif !important;
        font-weight: 300 !important;
        letter-spacing: 0.5px !important;
        color: var(--text-color) !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: var(--card-bg);
    }
    
    /* Cards */
    .stCard {
        background-color: var(--card-bg) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        border: 1px solid #222 !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease !important;
    }
    .stCard:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background-color: var(--card-bg);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #222;
        transition: transform 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
    }
    [data-testid="stMetricValue"] {
        font-family: 'Roboto', sans-serif !important;
        font-weight: 500 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid #333 !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        background-color: var(--hover-color) !important;
        border-color: var(--accent-color) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Inputs */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid #333 !important;
        border-radius: 4px !important;
    }
    
    /* Charts */
    .js-plotly-plot {
        background-color: var(--card-bg) !important;
    }
    .js-plotly-plot .plotly .modebar {
        background-color: transparent !important;
    }
    
    /* Tables */
    .stDataFrame {
        background-color: var(--card-bg) !important;
        border-radius: 8px !important;
    }
    .stDataFrame td, .stDataFrame th {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .element-container {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Custom classes */
    .tesla-card {
        background-color: var(--card-bg);
        border-radius: 8px;
        padding: 1.5rem;
        border: 1px solid #222;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .tesla-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* Status indicators */
    .status-up {
        color: var(--success-color) !important;
    }
    .status-down {
        color: var(--accent-color) !important;
    }
    .status-neutral {
        color: var(--warning-color) !important;
    }
    
    /* Auto-refresh animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    .live-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: var(--success-color);
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
</style>

<!-- Add auto-refresh meta tag -->
<meta http-equiv="refresh" content="5">

<!-- Add Tesla font -->
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Add live indicator to sidebar
st.sidebar.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
        <span class="live-indicator"></span>
        <span style="color: #00FF00; font-size: 0.8rem;">LIVE</span>
    </div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Select Page",
    ["Dashboard", "Portfolio Analysis", "Stock Predictions", "Crypto Analysis",
     "Risk Assessment", "ESG Analysis", "Options Analysis", "Market Regime",
     "Social Sentiment", "Technical Analysis", "Settings"]
)

# Import and show pages based on selection
if page == "Dashboard":
    from pages.dashboard import show_dashboard
    show_dashboard()
elif page == "Portfolio Analysis":
    from pages.portfolio import show_portfolio_analysis
    show_portfolio_analysis()
elif page == "Stock Predictions":
    from pages.predictions import show_stock_predictions
    show_stock_predictions()
elif page == "Crypto Analysis":
    from pages.crypto import show_crypto_analysis
    show_crypto_analysis()
elif page == "Risk Assessment":
    from pages.risk import show_risk_assessment
    show_risk_assessment()
elif page == "ESG Analysis":
    from pages.esg import show_esg_analysis
    show_esg_analysis()
elif page == "Options Analysis":
    from pages.options import show_options_analysis
    show_options_analysis()
elif page == "Market Regime":
    from pages.regime import show_market_regime
    show_market_regime()
elif page == "Social Sentiment":
    from pages.sentiment import show_social_sentiment
    show_social_sentiment()
elif page == "Technical Analysis":
    from pages.technical import show_technical_analysis
    show_technical_analysis()
elif page == "Settings":
    from pages.settings import show_settings
    show_settings()