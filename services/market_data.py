import yfinance as yf
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging
from functools import lru_cache
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketDataService:
    def __init__(self):
        self.price_cache = {}
        self.data_cache = {}
        
    @lru_cache(maxsize=100)
    def get_historical_data(self, symbol: str, period: str = '1y') -> pd.DataFrame:
        """Get historical market data with caching"""
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            
            if data.empty:
                return pd.DataFrame()
            
            # Calculate technical indicators
            data = self._add_technical_indicators(data)
            
            # Cache the data
            self.data_cache[symbol] = {
                'data': data,
                'timestamp': datetime.now()
            }
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def _add_technical_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Add technical indicators to the dataset"""
        # Moving averages
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
        data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
        
        # MACD
        data['MACD'] = data['EMA_12'] - data['EMA_26']
        data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
        
        # RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        data['BB_middle'] = data['Close'].rolling(window=20).mean()
        std = data['Close'].rolling(window=20).std()
        data['BB_upper'] = data['BB_middle'] + (std * 2)
        data['BB_lower'] = data['BB_middle'] - (std * 2)
        
        # Volume indicators
        data['Volume_SMA'] = data['Volume'].rolling(window=20).mean()
        data['Volume_Ratio'] = data['Volume'] / data['Volume_SMA']
        
        # Momentum indicators
        data['ROC'] = data['Close'].pct_change(periods=12) * 100
        data['MOM'] = data['Close'].diff(periods=10)
        
        # Volatility
        data['ATR'] = self._calculate_atr(data)
        
        # Fill NaN values
        data = data.fillna(method='ffill').fillna(method='bfill')
        
        return data
    
    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calculate Average True Range"""
        high = data['High']
        low = data['Low']
        close = data['Close']
        
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr
    
    def get_real_time_price(self, symbol: str) -> Optional[float]:
        """Get real-time price from cache"""
        try:
            # Check cache first
            if symbol in self.price_cache:
                cache_entry = self.price_cache[symbol]
                if datetime.now() - cache_entry['timestamp'] < timedelta(seconds=5):
                    return cache_entry['price']
            
            # Get latest price from yfinance
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d', interval='1m')
            
            if data.empty:
                return None
            
            price = data.iloc[-1].Close
            
            # Update cache
            self.price_cache[symbol] = {
                'price': price,
                'timestamp': datetime.now()
            }
            
            return price
            
        except Exception as e:
            logger.error(f"Error fetching price for {symbol}: {e}")
            return None
    
    def get_market_summary(self, symbols: List[str]) -> Dict:
        """Get market summary for given symbols"""
        summary = {}
        
        for symbol in symbols:
            try:
                data = self.get_historical_data(symbol)
                if not data.empty:
                    latest = data.iloc[-1]
                    prev_close = data.iloc[-2].Close if len(data) > 1 else latest.Close
                    
                    summary[symbol] = {
                        'price': self.get_real_time_price(symbol) or latest.Close,
                        'change': f"{((latest.Close / prev_close) - 1) * 100:.2f}%",
                        'volume': latest.Volume,
                        'rsi': latest.RSI,
                        'macd': latest.MACD,
                        'signal': 'Buy' if latest.MACD > latest.Signal_Line else 'Sell'
                    }
            except Exception as e:
                logger.error(f"Error getting summary for {symbol}: {e}")
                continue
        
        return summary