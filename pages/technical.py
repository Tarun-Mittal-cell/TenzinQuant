import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from services.market_data import MarketDataService

def show_technical_analysis():
    st.title("📊 Technical Analysis")
    
    # Initialize services
    market_data = MarketDataService()
    
    # Asset selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symbol = st.selectbox(
            "Select Asset",
            ["AAPL", "TSLA", "GOOGL", "MSFT", "AMZN", "BTC-USD", "ETH-USD"]
        )
    
    with col2:
        timeframe = st.selectbox(
            "Timeframe",
            ["1D", "4H", "1H", "15min"]
        )
    
    # Get technical data
    technical_data = market_data.get_technical_indicators(symbol)
    
    if technical_data is not None:
        # Price Chart with Indicators
        st.subheader("Price Action & Indicators")
        
        fig = go.Figure()
        
        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=technical_data.index,
            open=technical_data['Open'],
            high=technical_data['High'],
            low=technical_data['Low'],
            close=technical_data['Close'],
            name='Price'
        ))
        
        # Add moving averages
        fig.add_trace(go.Scatter(
            x=technical_data.index,
            y=technical_data['SMA_20'],
            name='SMA 20',
            line=dict(color='blue', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=technical_data.index,
            y=technical_data['SMA_50'],
            name='SMA 50',
            line=dict(color='orange', width=1)
        ))
        
        # Add Bollinger Bands
        fig.add_trace(go.Scatter(
            x=technical_data.index,
            y=technical_data['BB_upper'],
            name='BB Upper',
            line=dict(color='gray', width=1, dash='dash')
        ))
        
        fig.add_trace(go.Scatter(
            x=technical_data.index,
            y=technical_data['BB_lower'],
            name='BB Lower',
            line=dict(color='gray', width=1, dash='dash'),
            fill='tonexty'
        ))
        
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="Price",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Technical Indicators
        st.subheader("Technical Indicators")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "RSI (14)",
                f"{technical_data['RSI'].iloc[-1]:.1f}",
                "Neutral" if 40 < technical_data['RSI'].iloc[-1] < 60 else "Overbought" if technical_data['RSI'].iloc[-1] > 70 else "Oversold"
            )
        
        with col2:
            st.metric(
                "MACD",
                f"{technical_data['MACD'].iloc[-1]:.2f}",
                f"{technical_data['Signal'].iloc[-1]:.2f}"
            )
        
        with col3:
            st.metric(
                "BB Width",
                f"{(technical_data['BB_upper'].iloc[-1] - technical_data['BB_lower'].iloc[-1]) / technical_data['BB_middle'].iloc[-1]:.3f}",
                "High Volatility" if (technical_data['BB_upper'].iloc[-1] - technical_data['BB_lower'].iloc[-1]) / technical_data['BB_middle'].iloc[-1] > 0.1 else "Low Volatility"
            )
        
        # Support and Resistance Levels
        st.subheader("Support & Resistance Levels")
        
        levels = pd.DataFrame({
            'Level': ['Strong Resistance', 'Resistance', 'Current Price', 'Support', 'Strong Support'],
            'Price': [
                f"${technical_data['High'].max():.2f}",
                f"${technical_data['Close'].iloc[-1] * 1.02:.2f}",
                f"${technical_data['Close'].iloc[-1]:.2f}",
                f"${technical_data['Close'].iloc[-1] * 0.98:.2f}",
                f"${technical_data['Low'].min():.2f}"
            ],
            'Strength': ['High', 'Medium', '-', 'Medium', 'High']
        })
        
        st.dataframe(levels, hide_index=True)
        
        # Pattern Recognition
        st.subheader("Pattern Recognition")
        
        # Sample patterns (in real implementation, use pattern recognition algorithms)
        patterns = pd.DataFrame({
            'Pattern': ['Double Bottom', 'Golden Cross', 'RSI Divergence'],
            'Timeframe': ['4H', '1D', '1H'],
            'Reliability': ['High', 'Medium', 'Medium'],
            'Signal': ['Buy', 'Buy', 'Sell']
        })
        
        st.dataframe(patterns, hide_index=True)
        
        # Volume Analysis
        st.subheader("Volume Analysis")
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=technical_data.index,
            y=technical_data['Volume'],
            name='Volume',
            marker_color='rgb(158,202,225)',
            opacity=0.6
        ))
        
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="Volume"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Momentum Indicators
        st.subheader("Momentum Analysis")
        
        momentum_cols = st.columns(3)
        
        with momentum_cols[0]:
            st.metric(
                "Price ROC",
                f"{((technical_data['Close'].iloc[-1] / technical_data['Close'].iloc[-20]) - 1) * 100:.1f}%",
                "Strong" if ((technical_data['Close'].iloc[-1] / technical_data['Close'].iloc[-20]) - 1) > 0.05 else "Weak"
            )
        
        with momentum_cols[1]:
            st.metric(
                "Volume ROC",
                f"{((technical_data['Volume'].iloc[-1] / technical_data['Volume'].iloc[-20]) - 1) * 100:.1f}%",
                "Increasing" if technical_data['Volume'].iloc[-1] > technical_data['Volume'].mean() else "Decreasing"
            )
        
        with momentum_cols[2]:
            st.metric(
                "Trend Strength",
                "Strong" if abs(technical_data['Close'].iloc[-1] - technical_data['SMA_50'].iloc[-1]) > technical_data['Close'].std() else "Weak",
                f"{(technical_data['Close'].iloc[-1] - technical_data['SMA_50'].iloc[-1]) / technical_data['Close'].iloc[-1] * 100:.1f}%"
            )
    else:
        st.error("Unable to fetch technical data for the selected symbol.")