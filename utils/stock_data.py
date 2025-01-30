import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(symbol, period='1y'):
    """Fetch stock data from Yahoo Finance"""
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        return df, stock.info
    except Exception as e:
        return None, None

def calculate_metrics(df):
    """Calculate key financial metrics"""
    metrics = {}
    if df is not None and not df.empty:
        metrics['volatility'] = df['Close'].pct_change().std() * (252 ** 0.5)
        metrics['daily_returns'] = df['Close'].pct_change().mean()
        metrics['annual_returns'] = metrics['daily_returns'] * 252
        metrics['sharpe_ratio'] = metrics['annual_returns'] / metrics['volatility']
        
        # Calculate moving averages
        metrics['MA50'] = df['Close'].rolling(window=50).mean()
        metrics['MA200'] = df['Close'].rolling(window=200).mean()
        
    return metrics

def get_market_sentiment(symbol):
    """Get market news and trading volume analysis"""
    try:
        stock = yf.Ticker(symbol)
        news = stock.news
        volume = stock.history(period='1mo')['Volume'].mean()
        return news[:5], volume
    except:
        return [], 0
