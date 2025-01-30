import streamlit as st
import pandas as pd
import numpy as np
from models.quantum_predictor import QuantumPredictor
from services.market_data import MarketDataService
from utils.cache_manager import streamlit_cache, clear_cache
import yaml
import os
import asyncio
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Page configuration
st.set_page_config(
    page_title="Quantum Trading System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and futuristic design
st.markdown("""
<style>
    /* Dark theme */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    
    /* Neon accents */
    .stButton>button {
        background-color: #262730;
        color: #00FF9D;
        border: 1px solid #00FF9D;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00FF9D;
        color: #0E1117;
        box-shadow: 0 0 10px #00FF9D;
    }
    
    /* Metrics */
    .stMetric {
        background-color: #1E1E1E;
        border: 1px solid #00E5FF;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 0 5px #00E5FF;
    }
    
    /* Charts */
    .js-plotly-plot {
        background-color: #1E1E1E;
        border-radius: 5px;
        border: 1px solid #FF00E5;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #00FF9D;
        text-shadow: 0 0 5px #00FF9D;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #1E1E1E;
    }
</style>
""", unsafe_allow_html=True)

# Initialize services
@st.cache_resource
def init_services():
    return {
        'predictor': QuantumPredictor(),
        'market_data': MarketDataService()
    }

services = init_services()

@streamlit_cache(ttl_seconds=config['cache']['predictions'])
def get_predictions(symbols):
    """Get cached predictions"""
    return services['predictor'].get_predictions(symbols)

@streamlit_cache(ttl_seconds=config['cache']['stock_data'])
def get_market_summary(symbols):
    """Get cached market summary"""
    return services['market_data'].get_market_summary(symbols)

def main():
    st.title("🚀 Quantum Trading System")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["Dashboard", "Market Analysis", "AI Predictions", "Portfolio Optimization"]
    )
    
    # Default symbols
    symbols = st.sidebar.multiselect(
        "Select Stocks",
        ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN", "NVDA"],
        ["AAPL", "TSLA"]
    )
    
    if page == "Dashboard":
        show_dashboard(symbols)
    elif page == "Market Analysis":
        show_market_analysis(symbols)
    elif page == "AI Predictions":
        show_predictions(symbols)
    elif page == "Portfolio Optimization":
        show_portfolio_optimization(symbols)

def show_dashboard(symbols):
    st.header("Real-Time Market Dashboard")
    
    # Get market data
    market_data = get_market_summary(symbols)
    
    # Display metrics
    cols = st.columns(len(symbols))
    for i, symbol in enumerate(symbols):
        if symbol in market_data:
            data = market_data[symbol]
            with cols[i]:
                st.metric(
                    symbol,
                    f"${data['price']:.2f}",
                    data['change'],
                    delta_color="normal"
                )
    
    # Market overview
    st.subheader("Market Overview")
    col1, col2 = st.columns(2)
    
    with col1:
        # Price chart
        df = pd.DataFrame(market_data).T
        st.line_chart(df['price'])
        
    with col2:
        # Technical indicators
        st.dataframe(
            pd.DataFrame({
                'RSI': [data['rsi'] for data in market_data.values()],
                'MACD': [data['macd'] for data in market_data.values()],
                'Signal': [data['signal'] for data in market_data.values()]
            }, index=market_data.keys())
        )

def show_market_analysis(symbols):
    st.header("Advanced Market Analysis")
    
    # Get historical data
    data = services['market_data'].get_historical_data(symbols[0])
    
    # Technical analysis
    st.subheader("Technical Analysis")
    
    col1, col2 = st.columns(2)
    with col1:
        # Price and moving averages
        st.line_chart(data[['Close', 'SMA_20', 'SMA_50']])
        
    with col2:
        # RSI
        st.line_chart(data['RSI'])
    
    # Volume analysis
    st.subheader("Volume Analysis")
    st.bar_chart(data['Volume'])

def show_predictions(symbols):
    st.header("AI-Powered Predictions")
    
    # Get predictions
    predictions = get_predictions(symbols)
    
    # Display predictions
    for _, pred in predictions.iterrows():
        with st.container():
            cols = st.columns(5)
            cols[0].metric("Symbol", pred["Symbol"])
            cols[1].metric("Current", f"${pred['Current Price']:.2f}")
            cols[2].metric("Predicted", f"${pred['Predicted Price']:.2f}", pred["Change"])
            cols[3].metric("Confidence", pred["Confidence"])
            cols[4].metric("Signal", pred["Signal"])

def show_portfolio_optimization(symbols):
    st.header("Portfolio Optimization")
    
    # Get market data
    market_data = get_market_summary(symbols)
    
    # Display current portfolio
    st.subheader("Current Portfolio")
    portfolio_df = pd.DataFrame(market_data).T
    st.dataframe(portfolio_df)
    
    # Optimization controls
    st.subheader("Optimization Settings")
    risk_tolerance = st.slider("Risk Tolerance", 0.0, 1.0, 0.5)
    
    # Display optimization results
    st.subheader("Optimized Allocation")
    # Add optimization logic here

if __name__ == "__main__":
    main()