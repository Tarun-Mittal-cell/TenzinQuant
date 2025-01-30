import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from services.market_data import MarketDataService
from services.ai_analyst import AIAnalyst

def show_dashboard():
    # Initialize services
    market_data = MarketDataService()
    ai_analyst = AIAnalyst()
    
    # Get real-time data
    stock_data = market_data.get_real_time_stock_data()
    crypto_data = market_data.get_real_time_crypto_data()
    news = market_data.get_market_news()
    
    # Page title with live indicator
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 2rem;">
            <h1 style="margin: 0; margin-right: 1rem;">Quantum Trading Dashboard</h1>
            <div style="display: flex; align-items: center;">
                <span class="live-indicator"></span>
                <span style="color: #00FF00; font-size: 0.8rem;">LIVE DATA</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # AI Market Analysis
    st.markdown("""
        <div class="tesla-card">
            <h2 style="margin-top: 0;">🤖 AI Market Analysis</h2>
            <div style="color: #888; margin-bottom: 1rem;">
                Real-time analysis powered by GPT-4
            </div>
    """, unsafe_allow_html=True)
    
    analysis = ai_analyst.analyze_market_conditions(stock_data, news)
    st.markdown(f"<div style='color: #FFF;'>{analysis}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Market Overview
    st.markdown("<h2>📈 Market Overview</h2>", unsafe_allow_html=True)
    
    # Create metrics grid
    cols = st.columns(4)
    
    # Sample market indices with real-time data
    indices = {
        "S&P 500": market_data.get_real_time_stock_data(['^GSPC'])['^GSPC'],
        "NASDAQ": market_data.get_real_time_stock_data(['^IXIC'])['^IXIC'],
        "DOW": market_data.get_real_time_stock_data(['^DJI'])['^DJI'],
        "VIX": market_data.get_real_time_stock_data(['^VIX'])['^VIX']
    }
    
    for i, (index, data) in enumerate(indices.items()):
        change = data['change']
        change_color = "status-up" if change > 0 else "status-down"
        cols[i].markdown(f"""
            <div class="tesla-card" style="text-align: center;">
                <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">{index}</div>
                <div style="font-size: 1.5rem; font-weight: 500;">${data['price']:.2f}</div>
                <div class="{change_color}">{change:+.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Stock Watchlist
    st.markdown("<h2>📊 Stock Watchlist</h2>", unsafe_allow_html=True)
    
    # Create a grid for stock cards
    stock_cols = st.columns(3)
    for i, (symbol, data) in enumerate(stock_data.items()):
        change_color = "status-up" if data['change'] > 0 else "status-down"
        with stock_cols[i % 3]:
            st.markdown(f"""
                <div class="tesla-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0;">{symbol}</h3>
                        <div class="{change_color}" style="font-size: 1.1rem;">{data['change']:+.2f}%</div>
                    </div>
                    <div style="font-size: 1.5rem; margin: 1rem 0;">${data['price']:.2f}</div>
                    <div style="color: #888;">
                        Volume: {data['volume']:,.0f}<br>
                        Market Cap: ${data['market_cap']/1e9:.1f}B
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Crypto Overview
    st.markdown("<h2>💎 Crypto Overview</h2>", unsafe_allow_html=True)
    
    # Create a grid for crypto cards
    crypto_cols = st.columns(4)
    for i, (symbol, data) in enumerate(crypto_data.items()):
        change_color = "status-up" if data['change'] > 0 else "status-down"
        with crypto_cols[i % 4]:
            st.markdown(f"""
                <div class="tesla-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0;">{symbol.replace('-USD', '')}</h3>
                        <div class="{change_color}" style="font-size: 1.1rem;">{data['change']:+.2f}%</div>
                    </div>
                    <div style="font-size: 1.5rem; margin: 1rem 0;">${data['price']:.2f}</div>
                    <div style="color: #888;">
                        24h Volume: ${data['volume']:,.0f}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Latest News
    st.markdown("<h2>📰 Latest Market News</h2>", unsafe_allow_html=True)
    
    for item in news[:5]:
        st.markdown(f"""
            <div class="tesla-card" style="cursor: pointer;" onclick="window.open('{item['url']}', '_blank')">
                <h4 style="margin: 0; color: #FFF;">{item['headline']}</h4>
                <p style="margin: 0.5rem 0; color: #888;">{item['summary']}</p>
                <div style="color: #666; font-size: 0.8rem;">
                    {datetime.fromtimestamp(item['datetime']).strftime('%Y-%m-%d %H:%M:%S')}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
        <div style="margin-top: 2rem; padding: 1rem; background-color: #111; border-radius: 8px;">
            <p style="color: #666; font-size: 0.8rem; margin: 0;">
                Disclaimer: This platform is for informational purposes only. Not financial advice. 
                Trading carries risk. Past performance does not guarantee future results.
            </p>
        </div>
    """, unsafe_allow_html=True)