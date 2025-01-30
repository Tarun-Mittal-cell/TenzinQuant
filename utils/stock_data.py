import pandas as pd
import numpy as np
import yfinance as yf

class StockDataFetcher:
    def __init__(self):
        pass
        
    def get_stock_data(self, symbol, period='1y'):
        try:
            # Fetch data from Yahoo Finance
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)
            
            # Calculate technical indicators
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['RSI'] = self.calculate_rsi(data['Close'])
            data['MACD'] = self.calculate_macd(data['Close'])
            
            return data
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
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
    
    def get_company_info(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            return {
                'Name': info.get('longName', 'N/A'),
                'Sector': info.get('sector', 'N/A'),
                'Industry': info.get('industry', 'N/A'),
                'Market Cap': info.get('marketCap', 'N/A'),
                'PE Ratio': info.get('trailingPE', 'N/A'),
                'Dividend Yield': info.get('dividendYield', 'N/A')
            }
        except Exception as e:
            print(f"Error fetching company info for {symbol}: {str(e)}")
            return None