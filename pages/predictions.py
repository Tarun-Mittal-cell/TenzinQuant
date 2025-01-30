import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from models.quantum_predictor import QuantumPredictor

def show_stock_predictions():
    st.title("🔮 AI Stock Predictions")
    
    # Initialize predictor
    predictor = QuantumPredictor()
    
    # Stock selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symbols = st.multiselect(
            "Select stocks to analyze",
            ["AAPL", "GOOGL", "TSLA", "MSFT", "AMZN", "META", "NVDA"],
            ["AAPL", "TSLA"]
        )
    
    with col2:
        prediction_days = st.slider(
            "Prediction horizon (days)",
            min_value=1,
            max_value=30,
            value=7
        )
    
    if symbols:
        # Generate sample historical data
        dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
        
        for symbol in symbols:
            st.subheader(f"{symbol} Analysis")
            
            # Create tabs for different analyses
            tabs = st.tabs(["Price Prediction", "Technical Analysis", "Sentiment Analysis"])
            
            with tabs[0]:
                col1, col2, col3 = st.columns(3)
                
                # Generate sample predictions
                current_price = np.random.uniform(100, 1000)
                predicted_price = current_price * (1 + np.random.uniform(-0.05, 0.05))
                confidence = np.random.uniform(0.7, 0.95)
                
                with col1:
                    st.metric(
                        "Current Price",
                        f"${current_price:.2f}",
                        f"{((predicted_price/current_price - 1) * 100):.1f}%"
                    )
                with col2:
                    st.metric(
                        "Predicted Price",
                        f"${predicted_price:.2f}",
                        "7 days"
                    )
                with col3:
                    st.metric(
                        "AI Confidence",
                        f"{confidence:.1%}",
                        "High"
                    )
                
                # Price prediction chart
                prices = np.random.normal(current_price, current_price * 0.02, len(dates))
                prices = np.sort(prices)  # Make it trend upward
                
                # Generate future dates for prediction
                future_dates = pd.date_range(
                    start=datetime.now(),
                    periods=prediction_days,
                    freq='D'
                )
                
                # Generate predicted prices
                predicted_prices = np.linspace(
                    prices[-1],
                    predicted_price,
                    len(future_dates)
                )
                
                # Create prediction chart
                fig = go.Figure()
                
                # Historical prices
                fig.add_trace(go.Scatter(
                    x=dates,
                    y=prices,
                    mode='lines',
                    name='Historical',
                    line=dict(color='#00ff00', width=2)
                ))
                
                # Predicted prices
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=predicted_prices,
                    mode='lines',
                    name='Predicted',
                    line=dict(color='#ff9900', width=2, dash='dash')
                ))
                
                # Add confidence interval
                upper_bound = predicted_prices * (1 + (1 - confidence))
                lower_bound = predicted_prices * (1 - (1 - confidence))
                
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=upper_bound,
                    fill=None,
                    mode='lines',
                    line=dict(color='rgba(255,153,0,0)'),
                    showlegend=False
                ))
                
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=lower_bound,
                    fill='tonexty',
                    mode='lines',
                    line=dict(color='rgba(255,153,0,0)'),
                    name='Confidence Interval'
                ))
                
                fig.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=10, r=10, t=30, b=10)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with tabs[1]:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Technical indicators
                    indicators = pd.DataFrame({
                        'Indicator': ['RSI', 'MACD', 'SMA (20)', 'SMA (50)', 'Bollinger Bands'],
                        'Value': ['65.2', '1.23', '$152.30', '$148.50', 'Upper: $155.20'],
                        'Signal': ['Neutral', 'Buy', 'Buy', 'Buy', 'Overbought']
                    })
                    
                    st.dataframe(indicators, hide_index=True)
                
                with col2:
                    # Support/Resistance levels
                    levels = pd.DataFrame({
                        'Type': ['Resistance 2', 'Resistance 1', 'Support 1', 'Support 2'],
                        'Price': ['$158.50', '$155.20', '$148.80', '$145.30'],
                        'Strength': ['Strong', 'Moderate', 'Strong', 'Weak']
                    })
                    
                    st.dataframe(levels, hide_index=True)
            
            with tabs[2]:
                col1, col2 = st.columns(2)
                
                with col1:
                    # News sentiment
                    st.metric(
                        "News Sentiment",
                        "Positive",
                        "0.82",
                        help="Aggregated sentiment from news articles"
                    )
                    
                    news = pd.DataFrame({
                        'Source': ['Reuters', 'Bloomberg', 'CNBC'],
                        'Sentiment': ['Positive', 'Neutral', 'Positive'],
                        'Score': ['0.85', '0.52', '0.78']
                    })
                    
                    st.dataframe(news, hide_index=True)
                
                with col2:
                    # Social media sentiment
                    st.metric(
                        "Social Sentiment",
                        "Bullish",
                        "0.75",
                        help="Aggregated sentiment from social media"
                    )
                    
                    social = pd.DataFrame({
                        'Platform': ['Twitter', 'Reddit', 'StockTwits'],
                        'Sentiment': ['Bullish', 'Neutral', 'Bullish'],
                        'Score': ['0.88', '0.55', '0.82']
                    })
                    
                    st.dataframe(social, hide_index=True)
            
            st.divider()