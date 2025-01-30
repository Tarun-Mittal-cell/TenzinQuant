# Page config with modern theme
st.set_page_config(
    page_title="Tenzin Quantum - AI Stock Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

import streamlit as st
from utils.social_sentiment import MarketSentimentAnalyzer
from utils.nlp_analysis import analyze_news_sentiment
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from utils.stock_data import get_stock_data, calculate_metrics, get_market_sentiment
from utils.ml_models import StockPredictor
from utils.portfolio_optimizer import PortfolioOptimizer
from datetime import datetime, timedelta

# Add custom CSS for Tesla/SpaceX inspired theme
st.markdown("""
<style>
    /* Tesla-inspired dark theme */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }

    /* SpaceX-style headers */
    h1, h2, h3 {
        font-family: 'Roboto', sans-serif;
        color: #FFFFFF;
        font-weight: 500;
    }

    /* Tesla-style metrics container */
    .metric-container {
        background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid #333;
    }

    /* Futuristic accent colors */
    .highlight {
        color: #1DB954;
    }

    .warning {
        color: #FF4B4B;
    }

    /* SpaceX-style buttons */
    .stButton > button {
        background: linear-gradient(90deg, #1DB954, #147a38);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

def display_metrics(current_price, prediction, sentiment_score, sentiment_label):
    cols = st.columns(3)

    with cols[0]:
        st.markdown("""
        <div class="metric-container">
            <h3>Current Price</h3>
            <h2 style="color: #1DB954;">$%.2f</h2>
        </div>
        """ % current_price, unsafe_allow_html=True)

    with cols[1]:
        pred_delta = prediction - current_price
        delta_color = "#1DB954" if pred_delta >= 0 else "#FF4B4B"
        st.markdown(f"""
        <div class="metric-container">
            <h3>Predicted Price</h3>
            <h2 style="color: {delta_color};">$%.2f</h2>
            <p style="color: {delta_color};">%.2f</p>
        </div>
        """ % (prediction, pred_delta), unsafe_allow_html=True)

    with cols[2]:
        sentiment_color = "#1DB954" if sentiment_score >= 0 else "#FF4B4B"
        st.markdown(f"""
        <div class="metric-container">
            <h3>Market Sentiment</h3>
            <h2 style="color: {sentiment_color};">{sentiment_label}</h2>
            <p style="color: {sentiment_color};">%.2f</p>
        </div>
        """ % sentiment_score, unsafe_allow_html=True)

def create_stock_chart(df, metrics, symbol):
    fig = go.Figure()

    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='OHLC',
        increasing_line_color='#1DB954',
        decreasing_line_color='#FF4B4B'
    ))

    # Moving averages with modern styling
    fig.add_trace(go.Scatter(
        x=df.index,
        y=metrics['MA50'],
        name='MA50',
        line=dict(color='rgba(29, 185, 84, 0.8)', width=1.5, dash='dot'),
        hovertemplate='MA50: %{y:.2f}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=metrics['MA200'],
        name='MA200',
        line=dict(color='rgba(255, 255, 255, 0.8)', width=1.5, dash='dot'),
        hovertemplate='MA200: %{y:.2f}<extra></extra>'
    ))

    # Modern layout
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_rangeslider_visible=False,
        height=600,
        title={
            'text': f"{symbol} Stock Price",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24, color='#E2E2E2')
        },
        margin=dict(l=40, r=40, t=80, b=40),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0,0,0,0.5)'
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False
        )
    )

    return fig

# Load custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar with modern styling
st.sidebar.title("Tenzin Quantum")
st.sidebar.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <h4 style='color: #1DB954;'>AI-Powered Stock Analysis</h4>
</div>
""", unsafe_allow_html=True)

# Page selection
page = st.sidebar.selectbox("Select Page", ["Stock Analysis", "Portfolio Optimization"])

def display_sentiment_dashboard(symbol):
    st.markdown("<h2 style='text-align: center; color: #1DB954;'>🚀 Neural Link Sentiment Analysis</h2>", unsafe_allow_html=True)

    # Get news and analyze sentiment
    news, volume = get_market_sentiment(symbol)
    sentiment_analyzer = MarketSentimentAnalyzer()
    sentiment_data, metrics = sentiment_analyzer.analyze_market_sentiment(news)

    # Create futuristic metrics display
    cols = st.columns(4)

    # Neural Link Style Metrics
    metrics_display = [
        {"label": "Market Sentiment", "value": f"{metrics['overall_sentiment']:.2f}", "icon": "🌐"},
        {"label": "Momentum", "value": f"{metrics['sentiment_momentum']:.2f}", "icon": "📈"},
        {"label": "Impact Score", "value": f"{metrics['impact_score']:.1f}", "icon": "💫"},
        {"label": "AI Confidence", "value": f"{metrics['confidence']*100:.0f}%", "icon": "🧠"}
    ]

    for col, metric in zip(cols, metrics_display):
        with col:
            st.markdown(f"""
            <div class="metric-container">
                <h3>{metric['icon']} {metric['label']}</h3>
                <h2 class="highlight">{metric['value']}</h2>
            </div>
            """, unsafe_allow_html=True)

    # Create sentiment timeline
    if sentiment_data:
        df = pd.DataFrame(sentiment_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        fig = go.Figure()

        # Add main sentiment line
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['compound'],
            name='Market Sentiment',
            line=dict(color='#1DB954', width=2),
            mode='lines+markers'
        ))

        # Add confidence bands
        confidence_band = df['compound'].std()
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['compound'] + confidence_band,
            fill=None,
            mode='lines',
            line=dict(color='rgba(29, 185, 84, 0.1)'),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['compound'] - confidence_band,
            fill='tonexty',
            mode='lines',
            line=dict(color='rgba(29, 185, 84, 0.1)'),
            name='Confidence Band'
        ))

        # Update layout with futuristic theme
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title={
                'text': 'Neural Link Sentiment Timeline',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=24, color='#1DB954')
            },
            margin=dict(l=40, r=40, t=80, b=40),
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(255,255,255,0.1)',
                title='Timeline'
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(255,255,255,0.1)',
                title='Sentiment Strength'
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        # Display recent sentiment sources
        st.markdown("### 🔍 Recent Market Signals")
        for item in sentiment_data[:5]:  # Show last 5 items
            sentiment_color = "#1DB954" if item['compound'] > 0 else "#FF4B4B"
            st.markdown(f"""
            <div class="metric-container" style="margin-bottom: 10px;">
                <p style="color: {sentiment_color}; margin-bottom: 5px;">
                    {item['text']}
                </p>
                <small style="color: #666;">
                    {item['source']} | Impact: {item['impact_score']:.2f} | 
                    Sentiment: {item['compound']:.2f}
                </small>
            </div>
            """, unsafe_allow_html=True)


if page == "Stock Analysis":
    # Stock symbol input
    symbol = st.sidebar.text_input("Enter Stock Symbol", value="AAPL").upper()
    time_period = st.sidebar.selectbox(
        "Select Time Period",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=3
    )

    # Main content
    st.title(f"{symbol} Stock Analysis")

    # Fetch data
    df, stock_info = get_stock_data(symbol, time_period)

    if df is not None and not df.empty:
        # Initialize predictor
        predictor = StockPredictor()
        current_price = df['Close'].iloc[-1]

        # Train model and get prediction
        score = predictor.train(df)
        prediction = predictor.predict_next_day(df)

        # Get news and sentiment
        news, volume = get_market_sentiment(symbol)
        sentiment_score, sentiment_label, detailed_sentiments = analyze_news_sentiment(news)

        # Calculate metrics
        metrics = calculate_metrics(df)

        # Layout
        #Updated Metrics Display
        display_metrics(current_price, prediction, sentiment_score, sentiment_label)


        # Main chart
        fig = create_stock_chart(df, metrics, symbol)
        st.plotly_chart(fig, use_container_width=True)

        # Add the new sentiment dashboard after the metrics display
        display_sentiment_dashboard(symbol)

        # Enhanced Sentiment Analysis Section
        st.subheader("Market Sentiment Analysis")

        # Get detailed sentiment analysis
        news, volume = get_market_sentiment(symbol)
        sentiment_score, sentiment_label, detailed_sentiments = analyze_news_sentiment(news)

        # Create sentiment trend visualization
        if detailed_sentiments:
            sentiment_df = pd.DataFrame(detailed_sentiments)
            sentiment_df['datetime'] = pd.to_datetime(sentiment_df['timestamp'], unit='s')

            fig_sentiment = go.Figure()

            # Add sentiment trend line
            fig_sentiment.add_trace(go.Scatter(
                x=sentiment_df['datetime'],
                y=sentiment_df['compound'],
                name='Sentiment Score',
                line=dict(color='cyan', width=2)
            ))

            # Add positive/negative bands
            fig_sentiment.add_trace(go.Scatter(
                x=sentiment_df['datetime'],
                y=sentiment_df['positive'],
                name='Positive',
                fill=None,
                line=dict(color='green', width=1)
            ))

            fig_sentiment.add_trace(go.Scatter(
                x=sentiment_df['datetime'],
                y=sentiment_df['negative'],
                name='Negative',
                fill=None,
                line=dict(color='red', width=1)
            ))

            fig_sentiment.update_layout(
                template='plotly_dark',
                title='Sentiment Trend Analysis',
                xaxis_title='Date',
                yaxis_title='Sentiment Score',
                height=400
            )

            st.plotly_chart(fig_sentiment, use_container_width=True)

            # Source Credibility Analysis
            st.subheader("News Source Analysis")
            sources = set(s['source'] for s in detailed_sentiments)
            source_data = []

            def calculate_source_credibility(source, sentiments):
                # Placeholder function - replace with actual credibility calculation
                return np.random.rand()


            for source in sources:
                credibility = calculate_source_credibility(source, detailed_sentiments)
                source_data.append({
                    'Source': source,
                    'Credibility Score': f"{credibility:.2f}",
                    'Sentiment Impact': f"{np.mean([s['compound'] for s in detailed_sentiments if s['source'] == source]):.2f}"
                })

            source_df = pd.DataFrame(source_data)
            st.table(source_df)

        # Metrics and insights
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Key Metrics")
            metrics_df = pd.DataFrame({
                'Metric': ['Volatility', 'Annual Returns', 'Sharpe Ratio'],
                'Value': [
                    f"{metrics['volatility']:.2%}",
                    f"{metrics['annual_returns']:.2%}",
                    f"{metrics['sharpe_ratio']:.2f}"
                ]
            })
            st.table(metrics_df)

        with col2:
            st.subheader("AI Insights")
            insights = generate_insight(metrics, sentiment_label, prediction, current_price)
            for insight in insights:
                st.markdown(f"• {insight}")

        # Recent news
        st.subheader("Recent News")
        if news and isinstance(news, list):
            for article in news:
                if isinstance(article, dict):
                    title = article.get('title', 'No title available')
                    publisher = article.get('publisher', 'Unknown Publisher')
                    timestamp = article.get('providerPublishTime', None)

                    st.markdown(f"**{title}**")
                    if timestamp:
                        date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                        st.markdown(f"*{publisher}* - {date_str}")
                    else:
                        st.markdown(f"*{publisher}*")
                    st.markdown("---")
        else:
            st.info("No recent news available for this stock.")

    else:
        st.error("Unable to fetch data for the specified stock symbol. Please check the symbol and try again.")

else:  # Portfolio Optimization page
    st.title("Portfolio Optimization")

    # Portfolio input
    st.sidebar.subheader("Portfolio Settings")
    portfolio_symbols = st.sidebar.text_input(
        "Enter Stock Symbols (comma-separated)",
        value="AAPL,MSFT,GOOGL,AMZN"
    ).upper().split(',')

    # Initialize portfolio optimizer
    optimizer = PortfolioOptimizer(portfolio_symbols)
    optimizer.fetch_data()

    # Get optimal portfolio
    optimal_portfolio = optimizer.get_optimal_portfolio()

    # Display optimal allocation
    st.subheader("Optimal Portfolio Allocation")

    # Create columns for metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Expected Annual Return", f"{optimal_portfolio['expected_annual_return']:.2%}")
    with col2:
        st.metric("Annual Volatility", f"{optimal_portfolio['annual_volatility']:.2%}")
    with col3:
        st.metric("Sharpe Ratio", f"{optimal_portfolio['sharpe_ratio']:.2f}")

    # Display allocation weights
    weights_df = pd.DataFrame({
        'Stock': list(optimal_portfolio['weights'].keys()),
        'Weight': [f"{w:.2%}" for w in optimal_portfolio['weights'].values()]
    })

    st.subheader("Portfolio Weights")
    st.table(weights_df)

    # Generate and display efficient frontier
    st.subheader("Efficient Frontier")
    frontier_df = optimizer.efficient_frontier()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=frontier_df['volatility'],
        y=frontier_df['expected_return'],
        mode='lines',
        name='Efficient Frontier',
        line=dict(color='#1DB954', width=2)
    ))

    # Add current portfolio point
    fig.add_trace(go.Scatter(
        x=[optimal_portfolio['annual_volatility']],
        y=[optimal_portfolio['expected_annual_return']],
        mode='markers',
        name='Optimal Portfolio',
        marker=dict(size=12, color='#FF4B4B', symbol='star')
    ))

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title={
            'text': 'Efficient Frontier',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=24, color='#E2E2E2')
        },
        xaxis_title='Risk (Annual Volatility)',
        yaxis_title='Expected Annual Return',
        height=500,
        margin=dict(l=40, r=40, t=80, b=40),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0,0,0,0.5)'
        ),
        xaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(255,255,255,0.1)',
            zeroline=False
        )
    )

    st.plotly_chart(fig, use_container_width=True)