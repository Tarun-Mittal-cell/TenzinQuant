from openai import OpenAI
from transformers import pipeline
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class AIAnalyst:
    def __init__(self):
        self.client = OpenAI()  # Will automatically use OPENAI_API_KEY from environment
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        
    def analyze_market_conditions(self, market_data, news_data):
        """Analyze current market conditions using LLM"""
        try:
            # Prepare market summary
            market_summary = self._prepare_market_summary(market_data)
            news_summary = self._prepare_news_summary(news_data)
            
            # Create prompt for GPT
            messages = [
                {"role": "system", "content": "You are a highly skilled quantitative analyst with expertise in market analysis and trading."},
                {"role": "user", "content": f"""
                Analyze the current market conditions based on the following data:
                
                Market Data:
                {market_summary}
                
                Recent News:
                {news_summary}
                
                Provide a detailed analysis including:
                1. Overall market sentiment
                2. Key trends and patterns
                3. Potential risks and opportunities
                4. Trading recommendations
                
                Format the response in a clear, concise manner suitable for traders.
                """}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in market analysis: {str(e)}")
            return "Error analyzing market conditions. Using alternative data sources."
    
    def generate_trading_signals(self, symbol, technical_data, market_data, news_sentiment):
        """Generate trading signals using AI"""
        try:
            # Prepare technical analysis summary
            tech_summary = self._prepare_technical_summary(technical_data)
            
            messages = [
                {"role": "system", "content": "You are a professional trader with expertise in technical analysis and risk management."},
                {"role": "user", "content": f"""
                Analyze the trading opportunity for {symbol} based on the following data:
                
                Technical Analysis:
                {tech_summary}
                
                Market Data:
                Price: ${market_data.get('price', 0)}
                Change: {market_data.get('change', 0)}%
                Volume: {market_data.get('volume', 0)}
                
                News Sentiment: {news_sentiment}
                
                Provide specific trading recommendations including:
                1. Trading signal (Buy/Sell/Hold)
                2. Entry price points
                3. Stop loss levels
                4. Take profit targets
                5. Risk assessment
                """}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating trading signals: {str(e)}")
            return "Error generating trading signals. Using technical analysis only."
    
    def analyze_portfolio_risk(self, portfolio_data, market_conditions):
        """Analyze portfolio risk using AI"""
        try:
            portfolio_summary = self._prepare_portfolio_summary(portfolio_data)
            
            messages = [
                {"role": "system", "content": "You are a risk management expert with expertise in portfolio analysis."},
                {"role": "user", "content": f"""
                Analyze the portfolio risk based on the following data:
                
                Portfolio Composition:
                {portfolio_summary}
                
                Market Conditions:
                {market_conditions}
                
                Provide a comprehensive risk analysis including:
                1. Overall portfolio risk level
                2. Diversification assessment
                3. Sector exposure risks
                4. Correlation analysis
                5. Risk mitigation recommendations
                """}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error analyzing portfolio risk: {str(e)}")
            return "Error analyzing portfolio risk. Using standard risk metrics."
    
    def _prepare_market_summary(self, market_data):
        """Prepare market data summary"""
        summary = []
        for symbol, data in market_data.items():
            summary.append(f"{symbol}: ${data['price']:.2f} ({data['change']:.2f}%)")
        return "\n".join(summary)
    
    def _prepare_news_summary(self, news_data):
        """Prepare news summary"""
        summary = []
        for news in news_data[:5]:  # Latest 5 news items
            if isinstance(news, dict) and 'headline' in news:
                summary.append(f"- {news['headline']}")
        return "\n".join(summary)
    
    def _prepare_technical_summary(self, technical_data):
        """Prepare technical analysis summary"""
        if technical_data is None:
            return "No technical data available"
            
        try:
            latest = technical_data.iloc[-1]
            return f"""
            Price: ${latest['Close']:.2f}
            SMA20: ${latest['SMA_20']:.2f}
            SMA50: ${latest['SMA_50']:.2f}
            RSI: {latest['RSI']:.2f}
            MACD: {latest['MACD']:.2f}
            Signal: {latest['Signal']:.2f}
            Bollinger Bands:
            - Upper: ${latest['BB_upper']:.2f}
            - Middle: ${latest['BB_middle']:.2f}
            - Lower: ${latest['BB_lower']:.2f}
            """
        except Exception as e:
            print(f"Error preparing technical summary: {str(e)}")
            return "Technical data processing error"
    
    def _prepare_portfolio_summary(self, portfolio_data):
        """Prepare portfolio summary"""
        summary = []
        for symbol, data in portfolio_data.items():
            summary.append(f"{symbol}: {data['weight']*100:.1f}% (${data['value']:.2f})")
        return "\n".join(summary)
    
    def chat_with_ai_analyst(self, user_query, market_data=None, portfolio_data=None):
        """Interactive chat with AI analyst"""
        try:
            context = ""
            if market_data:
                context += f"\nMarket Data:\n{self._prepare_market_summary(market_data)}"
            if portfolio_data:
                context += f"\nPortfolio Data:\n{self._prepare_portfolio_summary(portfolio_data)}"
            
            messages = [
                {"role": "system", "content": "You are an AI financial analyst assistant, providing helpful insights and analysis to traders and investors."},
                {"role": "user", "content": f"""
                User Query: {user_query}
                
                Available Context:
                {context}
                
                Provide a helpful, informative response focusing on actionable insights and clear explanations.
                """}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in AI chat: {str(e)}")
            return "I apologize, but I'm having trouble processing your request at the moment. Please try again."