import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from services.market_data import MarketDataService
from services.ai_analyst import AIAnalyst

def show_crypto_analysis():
    st.title("🌐 Crypto Analysis")
    
    # Initialize services
    market_data = MarketDataService()
    ai_analyst = AIAnalyst()
    
    # Get real-time crypto data
    crypto_data = market_data.get_real_time_crypto_data()
    
    # Market Overview
    st.subheader("Crypto Market Overview")
    
    # Create metrics grid
    cols = st.columns(4)
    
    # Sample market data
    market_metrics = {
        "BTC Dominance": {"value": "52.3%", "change": "+0.5%"},
        "Total Market Cap": {"value": "$2.1T", "change": "+1.2%"},
        "24h Volume": {"value": "$98.5B", "change": "-3.2%"},
        "Fear & Greed": {"value": "65", "change": "Greed"}
    }
    
    for i, (metric, data) in enumerate(market_metrics.items()):
        cols[i].metric(
            metric,
            data["value"],
            data["change"]
        )
    
    # Price Action
    st.subheader("Price Action")
    
    # Create tabs for different timeframes
    timeframe_tabs = st.tabs(["24H", "7D", "30D", "YTD"])
    
    with timeframe_tabs[0]:
        # Sample price data
        dates = pd.date_range(end=datetime.now(), periods=24, freq='H')
        prices = pd.DataFrame({
            'BTC-USD': [45000 + i*100 + np.random.normal(0, 200) for i in range(24)],
            'ETH-USD': [2800 + i*10 + np.random.normal(0, 20) for i in range(24)],
            'SOL-USD': [100 + i + np.random.normal(0, 2) for i in range(24)]
        }, index=dates)
        
        fig = go.Figure()
        
        for col in prices.columns:
            fig.add_trace(go.Scatter(
                x=prices.index,
                y=prices[col],
                name=col,
                mode='lines'
            ))
        
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Time",
            yaxis_title="Price (USD)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Trading Signals
    st.subheader("AI Trading Signals")
    
    signals = pd.DataFrame({
        'Asset': ['BTC-USD', 'ETH-USD', 'SOL-USD', 'ADA-USD'],
        'Signal': ['Strong Buy', 'Buy', 'Hold', 'Sell'],
        'Confidence': ['95%', '85%', '75%', '80%'],
        'Target': ['$48,500', '$3,200', '$105', '$0.45']
    })
    
    st.dataframe(
        signals,
        hide_index=True,
        column_config={
            'Asset': 'Asset',
            'Signal': 'Signal',
            'Confidence': 'AI Confidence',
            'Target': 'Price Target'
        }
    )
    
    # Technical Analysis
    st.subheader("Technical Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Technical indicators
        indicators = pd.DataFrame({
            'Indicator': ['RSI', 'MACD', 'MA Cross', 'BB Width'],
            'Value': ['65.2', '235.5', 'Bullish', '0.15'],
            'Signal': ['Neutral', 'Buy', 'Buy', 'High Vol']
        })
        
        st.dataframe(indicators, hide_index=True)
    
    with col2:
        # Support/Resistance levels
        levels = pd.DataFrame({
            'Level': ['R2', 'R1', 'S1', 'S2'],
            'Price': ['$47,500', '$46,200', '$44,800', '$43,500'],
            'Strength': ['Strong', 'Moderate', 'Strong', 'Weak']
        })
        
        st.dataframe(levels, hide_index=True)
    
    # On-Chain Analysis
    st.subheader("On-Chain Analysis")
    
    metrics_cols = st.columns(3)
    
    with metrics_cols[0]:
        st.metric(
            "Active Addresses",
            "1.2M",
            "+5.2%",
            help="24h active addresses"
        )
    with metrics_cols[1]:
        st.metric(
            "Network Hash Rate",
            "245 EH/s",
            "+2.8%",
            help="Bitcoin network hash rate"
        )
    with metrics_cols[2]:
        st.metric(
            "Exchange Outflows",
            "25.5K BTC",
            "+15.2%",
            help="24h exchange outflows"
        )
    
    # Market Sentiment
    st.subheader("Market Sentiment Analysis")
    
    # Sample sentiment data
    sentiment_data = pd.DataFrame({
        'Source': ['Twitter', 'Reddit', 'Trading View', 'News'],
        'Sentiment': [0.75, 0.65, 0.80, 0.70]
    })
    
    fig = px.bar(
        sentiment_data,
        x='Source',
        y='Sentiment',
        color='Sentiment',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # AI Market Analysis
    st.subheader("AI Market Analysis")
    
    analysis = ai_analyst.analyze_market_conditions(crypto_data, [])
    st.markdown(f"<div style='background-color: #1E1E1E; padding: 20px; border-radius: 10px;'>{analysis}</div>", unsafe_allow_html=True)
    
    # Correlation Matrix
    st.subheader("Crypto Correlations")
    
    # Sample correlation data
    corr_data = pd.DataFrame(
        [[1.0, 0.8, 0.7, 0.6],
         [0.8, 1.0, 0.8, 0.7],
         [0.7, 0.8, 1.0, 0.8],
         [0.6, 0.7, 0.8, 1.0]],
        columns=['BTC', 'ETH', 'SOL', 'ADA'],
        index=['BTC', 'ETH', 'SOL', 'ADA']
    )
    
    fig = px.imshow(
        corr_data,
        color_continuous_scale='RdBu',
        aspect='auto'
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)