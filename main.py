import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from utils.stock_data import get_stock_data, calculate_metrics, get_market_sentiment
from utils.ml_models import StockPredictor
from utils.nlp_analysis import analyze_news_sentiment, generate_insight
from utils.portfolio_optimizer import PortfolioOptimizer

# Page config
st.set_page_config(
    page_title="Tenzin Quantum - AI Stock Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Tenzin Quantum")
st.sidebar.markdown("AI-Powered Stock Analysis")

# Page selection
page = st.sidebar.selectbox("Select Page", ["Stock Analysis", "Portfolio Optimization"])

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
        sentiment_score, sentiment_label = analyze_news_sentiment(news)

        # Calculate metrics
        metrics = calculate_metrics(df)

        # Layout
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Current Price", f"${current_price:.2f}")
        with col2:
            pred_delta = prediction - current_price
            st.metric("Predicted Price", f"${prediction:.2f}", f"{pred_delta:.2f}")
        with col3:
            st.metric("Market Sentiment", sentiment_label, f"{sentiment_score:.2f}")

        # Main chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        ))

        fig.add_trace(go.Scatter(
            x=df.index,
            y=metrics['MA50'],
            name='MA50',
            line=dict(color='orange', width=1)
        ))

        fig.add_trace(go.Scatter(
            x=df.index,
            y=metrics['MA200'],
            name='MA200',
            line=dict(color='blue', width=1)
        ))

        fig.update_layout(
            template='plotly_dark',
            xaxis_rangeslider_visible=False,
            height=600,
            title=f"{symbol} Stock Price"
        )

        st.plotly_chart(fig, use_container_width=True)

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
        x=frontier_df['risk'],
        y=frontier_df['return'],
        mode='lines',
        name='Efficient Frontier'
    ))

    # Add current portfolio point
    fig.add_trace(go.Scatter(
        x=[optimal_portfolio['annual_volatility']],
        y=[optimal_portfolio['expected_annual_return']],
        mode='markers',
        name='Optimal Portfolio',
        marker=dict(size=10, color='red')
    ))

    fig.update_layout(
        template='plotly_dark',
        title='Efficient Frontier',
        xaxis_title='Risk (Annual Volatility)',
        yaxis_title='Expected Annual Return',
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)