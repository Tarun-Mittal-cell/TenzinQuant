import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from services.market_data import MarketDataService
from services.ai_analyst import AIAnalyst

def show_social_sentiment():
    st.title("📱 Social Sentiment Analysis")
    
    # Initialize services
    market_data = MarketDataService()
    ai_analyst = AIAnalyst()
    
    # Overall Market Sentiment
    st.subheader("Overall Market Sentiment")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Market Sentiment",
            "Bullish",
            "+0.82",
            help="Aggregated sentiment from all sources"
        )
    with col2:
        st.metric(
            "Social Media",
            "Very Bullish",
            "+0.88",
            help="Twitter, Reddit, StockTwits sentiment"
        )
    with col3:
        st.metric(
            "News Sentiment",
            "Neutral",
            "+0.52",
            help="News and media sentiment"
        )
    with col4:
        st.metric(
            "Fear & Greed",
            "65",
            "Greed",
            help="Market Fear & Greed Index"
        )
    
    # Trending Assets
    st.subheader("Trending Assets")
    
    trending = pd.DataFrame({
        'Asset': ['TSLA', 'AAPL', 'NVDA', 'BTC', 'MSFT'],
        'Mentions': [15000, 12000, 8000, 7500, 6000],
        'Sentiment': [0.85, 0.75, 0.90, 0.65, 0.80],
        'Change': ['+25%', '+15%', '+40%', '-5%', '+10%']
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=trending['Asset'],
        y=trending['Mentions'],
        name='Mentions',
        marker_color=trending['Sentiment'],
        marker=dict(
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title='Sentiment')
        )
    ))
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Asset",
        yaxis_title="Social Media Mentions"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Sentiment by Platform
    st.subheader("Sentiment by Platform")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Platform sentiment
        platforms = pd.DataFrame({
            'Platform': ['Twitter', 'Reddit', 'StockTwits', 'YouTube', 'News'],
            'Bullish': [65, 55, 70, 60, 50],
            'Neutral': [20, 30, 15, 25, 35],
            'Bearish': [15, 15, 15, 15, 15]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Bullish',
            x=platforms['Platform'],
            y=platforms['Bullish'],
            marker_color='#00ff00'
        ))
        
        fig.add_trace(go.Bar(
            name='Neutral',
            x=platforms['Platform'],
            y=platforms['Neutral'],
            marker_color='#888888'
        ))
        
        fig.add_trace(go.Bar(
            name='Bearish',
            x=platforms['Platform'],
            y=platforms['Bearish'],
            marker_color='#ff0000'
        ))
        
        fig.update_layout(
            barmode='stack',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sentiment trends
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        sentiment_trend = pd.DataFrame({
            'Date': dates,
            'Sentiment': np.cumsum(np.random.normal(0, 0.1, size=len(dates))) + 0.7
        })
        
        fig = px.line(
            sentiment_trend,
            x='Date',
            y='Sentiment',
            title='30-Day Sentiment Trend'
        )
        
        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Key Topics
    st.subheader("Trending Topics")
    
    topics = pd.DataFrame({
        'Topic': ['AI/ML', 'Interest Rates', 'Crypto Regulation', 'Tech Earnings', 'China Market'],
        'Mentions': [25000, 18000, 15000, 12000, 10000],
        'Sentiment': [0.85, -0.2, 0.3, 0.6, -0.1]
    })
    
    fig = px.scatter(
        topics,
        x='Mentions',
        y='Sentiment',
        size='Mentions',
        text='Topic',
        color='Sentiment',
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_traces(
        textposition='top center',
        marker=dict(sizeref=2.*max(topics['Mentions'])/(40.**2))
    )
    
    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # News Analysis
    st.subheader("Latest Market News")
    
    news = market_data.get_market_news()
    
    for item in news[:5]:
        sentiment_score = np.random.uniform(-1, 1)  # Simulated sentiment score
        sentiment_color = 'green' if sentiment_score > 0.2 else 'red' if sentiment_score < -0.2 else 'gray'
        
        st.markdown(f"""
            <div style='background-color: #1E1E1E; padding: 15px; border-radius: 10px; margin: 10px 0;'>
                <h4 style='margin: 0; color: white;'>{item['headline']}</h4>
                <p style='margin: 5px 0; color: #888888;'>{item['summary']}</p>
                <p style='margin: 0; color: {sentiment_color};'>
                    Sentiment: {sentiment_score:.2f}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Sentiment Alerts
    st.subheader("Sentiment Alerts")
    
    alerts = pd.DataFrame({
        'Asset': ['NVDA', 'TSLA', 'AAPL', 'GOOGL'],
        'Alert Type': ['Sentiment Spike', 'Unusual Activity', 'News Impact', 'Social Momentum'],
        'Priority': ['High', 'Medium', 'Low', 'Medium'],
        'Action': ['Monitor', 'Research', 'Monitor', 'Research']
    })
    
    st.dataframe(alerts, hide_index=True)
    
    # AI Analysis
    st.subheader("AI Sentiment Analysis")
    
    analysis = ai_analyst.analyze_market_conditions({}, news)
    st.markdown(f"<div style='background-color: #1E1E1E; padding: 20px; border-radius: 10px;'>{analysis}</div>", unsafe_allow_html=True)
    
    # Sentiment-based Trading Signals
    st.subheader("Trading Signals")
    
    signals = pd.DataFrame({
        'Asset': ['TSLA', 'AAPL', 'NVDA', 'MSFT'],
        'Signal': ['Strong Buy', 'Hold', 'Buy', 'Buy'],
        'Sentiment Score': [0.85, 0.55, 0.75, 0.70],
        'Confidence': ['High', 'Medium', 'High', 'Medium']
    })
    
    st.dataframe(signals, hide_index=True)