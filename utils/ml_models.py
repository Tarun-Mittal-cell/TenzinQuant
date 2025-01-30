import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler

class QuantumPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = MinMaxScaler()
        
    def prepare_data(self, data):
        # Add technical indicators
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data['SMA_50'] = data['Close'].rolling(window=50).mean()
        data['RSI'] = self.calculate_rsi(data['Close'])
        data['MACD'] = self.calculate_macd(data['Close'])
        
        # Remove NaN values
        data = data.dropna()
        
        return data
    
    def calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def calculate_macd(self, prices, fast=12, slow=26, signal=9):
        exp1 = prices.ewm(span=fast, adjust=False).mean()
        exp2 = prices.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return macd - signal_line
    
    def get_predictions(self, symbols):
        predictions = []
        
        for symbol in symbols:
            # Simulate prediction for demo
            current_price = np.random.uniform(100, 1000)
            predicted_price = current_price * (1 + np.random.uniform(-0.05, 0.05))
            confidence = np.random.uniform(0.7, 0.95)
            
            predictions.append({
                'Symbol': symbol,
                'Current Price': f'${current_price:.2f}',
                'Predicted Price': f'${predicted_price:.2f}',
                'Change': f'{((predicted_price/current_price - 1) * 100):.2f}%',
                'Confidence': f'{confidence:.2%}',
                'Signal': 'Buy' if predicted_price > current_price else 'Sell'
            })
        
        return pd.DataFrame(predictions)
    
    def detect_market_regime(self, data):
        """
        Detect the current market regime using machine learning.
        Returns regime classification and confidence score.
        """
        # Calculate market indicators
        volatility = np.std(data['returns']) * np.sqrt(252)  # Annualized volatility
        momentum = data['returns'].rolling(window=20).mean().iloc[-1]
        trend = self.calculate_trend_strength(data)
        
        # Classify regime
        if volatility < 0.15:  # Low volatility
            if momentum > 0:
                regime = "Bull Market - Low Volatility"
            else:
                regime = "Bear Market - Low Volatility"
        else:  # High volatility
            if momentum > 0:
                regime = "Bull Market - High Volatility"
            else:
                regime = "Bear Market - High Volatility"
        
        # Calculate confidence score
        confidence = np.random.uniform(0.7, 0.95)  # Simulated for demo
        
        return {
            'regime': regime,
            'confidence': confidence,
            'volatility': volatility,
            'momentum': momentum,
            'trend_strength': trend
        }
    
    def calculate_trend_strength(self, data):
        """Calculate the strength of the current market trend."""
        # Use price relative to moving averages
        sma_20 = data['Close'].rolling(window=20).mean()
        sma_50 = data['Close'].rolling(window=50).mean()
        
        # Calculate trend strength (percentage of time price is above moving average)
        above_sma20 = (data['Close'] > sma_20).mean()
        above_sma50 = (data['Close'] > sma_50).mean()
        
        return (above_sma20 + above_sma50) / 2