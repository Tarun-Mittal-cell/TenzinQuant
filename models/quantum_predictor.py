import numpy as np
import pandas as pd
from typing import List, Dict, Union
import torch
import torch.nn as nn
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import xgboost as xgb
import lightgbm as lgb
from sklearn.preprocessing import StandardScaler
import logging
import yfinance as yf
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LSTMModel(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, num_layers: int, dropout: float):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, dropout=dropout, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)
        
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])

class TransformerModel(nn.Module):
    def __init__(self, input_dim: int, d_model: int, nhead: int, num_layers: int):
        super().__init__()
        self.embedding = nn.Linear(input_dim, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc = nn.Linear(d_model, 1)
        
    def forward(self, x):
        x = self.embedding(x)
        x = self.transformer(x)
        return self.fc(x.mean(dim=1))

class QuantumPredictor:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.scaler = StandardScaler()
        self.models = self._initialize_models()
        
    def _initialize_models(self) -> Dict:
        models = {}
        
        # LSTM model
        models['lstm'] = LSTMModel(
            input_dim=10,
            hidden_dim=64,
            num_layers=2,
            dropout=0.2
        ).to(self.device)
        
        # Transformer model
        models['transformer'] = TransformerModel(
            input_dim=10,
            d_model=64,
            nhead=4,
            num_layers=2
        ).to(self.device)
        
        # XGBoost model
        models['xgboost'] = xgb.XGBRegressor(
            max_depth=6,
            learning_rate=0.1,
            n_estimators=100,
            objective='reg:squarederror',
            tree_method='hist'
        )
        
        # LightGBM model
        models['lightgbm'] = lgb.LGBMRegressor(
            num_leaves=31,
            learning_rate=0.05,
            n_estimators=100
        )
        
        return models
    
    def _get_market_data(self, symbol: str) -> pd.DataFrame:
        """Get market data with technical indicators"""
        try:
            # Get historical data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1y')
            
            if data.empty:
                return None
            
            # Calculate technical indicators
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['RSI'] = self._calculate_rsi(data['Close'])
            data['MACD'] = self._calculate_macd(data['Close'])
            data['Volume_MA'] = data['Volume'].rolling(window=20).mean()
            data['Returns'] = data['Close'].pct_change()
            data['Volatility'] = data['Returns'].rolling(window=20).std()
            
            # Forward fill NaN values
            data = data.fillna(method='ffill')
            
            return data
            
        except Exception as e:
            logger.error(f"Error getting market data for {symbol}: {e}")
            return None
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def _calculate_macd(self, prices: pd.Series) -> pd.Series:
        """Calculate MACD"""
        exp1 = prices.ewm(span=12, adjust=False).mean()
        exp2 = prices.ewm(span=26, adjust=False).mean()
        return exp1 - exp2
    
    def _prepare_features(self, data: pd.DataFrame) -> torch.Tensor:
        """Prepare features for prediction"""
        features = np.column_stack([
            data['Returns'].values,
            data['SMA_20'].values / data['Close'].values - 1,
            data['SMA_50'].values / data['Close'].values - 1,
            data['RSI'].values / 100,
            data['MACD'].values,
            data['Volume'].values / data['Volume_MA'].values,
            data['Volatility'].values,
            data['High'].values / data['Close'].values - 1,
            data['Low'].values / data['Close'].values - 1,
            data['Open'].values / data['Close'].values - 1
        ])
        
        # Scale features
        features = self.scaler.fit_transform(features)
        
        # Convert to tensor
        return torch.FloatTensor(features).unsqueeze(0)
    
    def _generate_signal(self, current_price: float, predicted_price: float) -> str:
        """Generate trading signal"""
        percent_change = (predicted_price / current_price - 1) * 100
        
        if percent_change > 2:
            return "Strong Buy"
        elif percent_change > 0.5:
            return "Buy"
        elif percent_change < -2:
            return "Strong Sell"
        elif percent_change < -0.5:
            return "Sell"
        else:
            return "Hold"
    
    def get_predictions(self, symbols: List[str]) -> pd.DataFrame:
        """Get predictions for multiple symbols"""
        predictions = []
        
        for symbol in symbols:
            try:
                # Get market data
                data = self._get_market_data(symbol)
                if data is None or len(data) < 50:  # Need sufficient history
                    continue
                
                # Prepare features
                features = self._prepare_features(data)
                
                # Get current price
                current_price = data['Close'].iloc[-1]
                
                # Get predictions from each model
                with torch.no_grad():
                    lstm_pred = self.models['lstm'](features.to(self.device)).cpu().numpy()[0, 0]
                    transformer_pred = self.models['transformer'](features.to(self.device)).cpu().numpy()[0, 0]
                
                xgb_pred = self.models['xgboost'].predict(features.squeeze(0).cpu().numpy())[-1]
                lgb_pred = self.models['lightgbm'].predict(features.squeeze(0).cpu().numpy())[-1]
                
                # Combine predictions
                weights = [0.3, 0.3, 0.2, 0.2]  # LSTM, Transformer, XGBoost, LightGBM
                predicted_price = np.average(
                    [lstm_pred, transformer_pred, xgb_pred, lgb_pred],
                    weights=weights
                ) * current_price
                
                # Calculate confidence based on model agreement
                preds = [lstm_pred, transformer_pred, xgb_pred, lgb_pred]
                confidence = 100 * (1 - np.std(preds) / np.mean(preds))
                
                # Generate signal
                signal = self._generate_signal(current_price, predicted_price)
                
                predictions.append({
                    'Symbol': symbol,
                    'Current Price': current_price,
                    'Predicted Price': predicted_price,
                    'Change': f"{((predicted_price / current_price) - 1) * 100:.2f}%",
                    'Confidence': f"{min(max(confidence, 0), 100):.1f}%",
                    'Signal': signal
                })
                
            except Exception as e:
                logger.error(f"Error predicting for {symbol}: {e}")
                continue
        
        return pd.DataFrame(predictions)