import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

class StockPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = MinMaxScaler()
        
    def prepare_data(self, df):
        """Prepare data for prediction"""
        df = df.copy()
        
        # Create features
        df['SMA_5'] = df['Close'].rolling(window=5).mean()
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['RSI'] = self.calculate_rsi(df['Close'])
        df['Price_Change'] = df['Close'].pct_change()
        df['Volume_Change'] = df['Volume'].pct_change()
        
        # Drop NaN values
        df.dropna(inplace=True)
        
        return df
    
    def calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def create_features(self, df):
        """Create feature matrix X and target vector y"""
        X = df[['SMA_5', 'SMA_20', 'RSI', 'Price_Change', 'Volume_Change']].values
        y = df['Close'].values
        
        X = self.scaler.fit_transform(X)
        return X, y
    
    def train(self, df):
        """Train the model"""
        prepared_data = self.prepare_data(df)
        X, y = self.create_features(prepared_data)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        return self.model.score(X_test, y_test)
    
    def predict_next_day(self, df):
        """Predict the next day's closing price"""
        prepared_data = self.prepare_data(df)
        X, _ = self.create_features(prepared_data)
        
        last_features = X[-1].reshape(1, -1)
        prediction = self.model.predict(last_features)[0]
        
        return prediction
