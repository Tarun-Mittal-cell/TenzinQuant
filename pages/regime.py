import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from services.market_data import MarketDataService
from services.ai_analyst import AIAnalyst

def show_market_regime():
    st.title("🎯 Market Regime Detection")
    
    # Initialize services
    market_data = MarketDataService()
    ai_analyst = AIAnalyst()
    
    # Get market data
    stock_data = market_data.get_real_time_stock_data()
    
    # Current Regime
    st.subheader("Current Market Regime")
    
    # Sample regime data
    regime_data = {
        'regime': 'Bull Market - High Volatility',
        'confidence': 0.85,
        'volatility': 0.25,
        'trend': 0.15,
        'momentum': 0.08
    }
    
    # Display regime metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Regime",
            regime_data['regime'],
            f"{regime_data['confidence']*100:.1f}% Confidence"
        )
    with col2:
        st.metric(
            "Volatility",
            f"{regime_data['volatility']*100:.1f}%",
            "High" if regime_data['volatility'] > 0.2 else "Low"
        )
    with col3:
        st.metric(
            "Trend",
            f"{regime_data['trend']*100:.1f}%",
            "Bullish" if regime_data['trend'] > 0 else "Bearish"
        )
    with col4:
        st.metric(
            "Momentum",
            f"{regime_data['momentum']*100:.1f}%",
            "Strong" if abs(regime_data['momentum']) > 0.05 else "Weak"
        )
    
    # Regime History
    st.subheader("Regime History")
    
    # Sample historical regime data
    dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
    regimes = np.random.choice(
        ['Bull - Low Vol', 'Bull - High Vol', 'Bear - Low Vol', 'Bear - High Vol'],
        size=len(dates),
        p=[0.4, 0.3, 0.2, 0.1]
    )
    
    regime_history = pd.DataFrame({
        'Date': dates,
        'Regime': regimes,
        'Confidence': np.random.uniform(0.7, 0.95, size=len(dates))
    })
    
    fig = go.Figure()
    
    for regime in regime_history['Regime'].unique():
        mask = regime_history['Regime'] == regime
        fig.add_trace(go.Scatter(
            x=regime_history[mask]['Date'],
            y=regime_history[mask]['Confidence'],
            name=regime,
            mode='lines',
            line=dict(width=2)
        ))
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Date",
        yaxis_title="Regime Confidence",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Market Indicators
    st.subheader("Market Indicators")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Technical indicators
        indicators = pd.DataFrame({
            'Indicator': ['VIX', 'Put/Call Ratio', 'Advance/Decline', 'New Highs/Lows'],
            'Value': ['22.5', '0.85', '1.2', '2.5'],
            'Signal': ['Elevated', 'Neutral', 'Bullish', 'Bullish']
        })
        
        st.dataframe(indicators, hide_index=True)
    
    with col2:
        # Market breadth
        breadth = pd.DataFrame({
            'Metric': ['Stocks Above 200 MA', 'Stocks Above 50 MA', 'RSI > 70', 'RSI < 30'],
            'Value': ['65%', '55%', '15%', '10%']
        })
        
        st.dataframe(breadth, hide_index=True)
    
    # Sector Analysis
    st.subheader("Sector Performance")
    
    # Sample sector data
    sectors = ['Technology', 'Healthcare', 'Financials', 'Energy', 'Consumer', 'Industrials']
    performance = np.random.uniform(-5, 8, size=len(sectors))
    
    sector_data = pd.DataFrame({
        'Sector': sectors,
        'Performance': performance
    })
    
    fig = px.bar(
        sector_data,
        x='Sector',
        y='Performance',
        color='Performance',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # AI Analysis
    st.subheader("AI Market Analysis")
    
    analysis = ai_analyst.analyze_market_conditions(stock_data, [])
    st.markdown(f"<div style='background-color: #1E1E1E; padding: 20px; border-radius: 10px;'>{analysis}</div>", unsafe_allow_html=True)
    
    # Trading Recommendations
    st.subheader("Regime-Based Trading Recommendations")
    
    recommendations = pd.DataFrame({
        'Asset Class': ['Stocks', 'Bonds', 'Commodities', 'Crypto'],
        'Allocation': ['Overweight', 'Underweight', 'Neutral', 'Overweight'],
        'Risk Level': ['High', 'Low', 'Medium', 'High'],
        'Strategy': ['Momentum', 'Defensive', 'Tactical', 'Trend Following']
    })
    
    st.dataframe(recommendations, hide_index=True)
    
    # Risk Metrics
    st.subheader("Regime-Specific Risk Metrics")
    
    risk_cols = st.columns(3)
    
    with risk_cols[0]:
        st.metric(
            "Portfolio Beta",
            "1.2",
            "+0.2",
            help="Portfolio sensitivity to market movements"
        )
    
    with risk_cols[1]:
        st.metric(
            "Correlation",
            "0.85",
            "+0.05",
            help="Cross-asset correlation"
        )
    
    with risk_cols[2]:
        st.metric(
            "Tail Risk",
            "High",
            "⚠️",
            help="Risk of extreme market events"
        )