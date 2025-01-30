import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

class MarketSentimentAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()

    def analyze_text_sentiment(self, texts, sources=None):
        """Analyze sentiment of text data with Tesla-style metrics"""
        sentiment_data = []

        for i, text in enumerate(texts):
            sentiment = self.sia.polarity_scores(text)
            sentiment_data.append({
                'timestamp': datetime.now() - timedelta(hours=i),
                'compound': sentiment['compound'],
                'impact_score': len(text.split()) / 100,  # Simple impact score based on length
                'source': sources[i] if sources else 'Market News',
                'text': text
            })

        return sentiment_data

    def get_aggregated_sentiment(self, sentiment_data):
        """Get Tesla-style sentiment metrics"""
        if not sentiment_data:
            return {
                'overall_sentiment': 0,
                'sentiment_momentum': 0,
                'impact_score': 0,
                'confidence': 0
            }

        df = pd.DataFrame(sentiment_data)

        # Calculate weighted sentiment based on impact
        total_impact = df['impact_score'].sum()
        if total_impact > 0:
            weighted_sentiment = (df['compound'] * df['impact_score']).sum() / total_impact
        else:
            weighted_sentiment = df['compound'].mean()

        # Calculate sentiment momentum (change over time)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        sentiment_change = df['compound'].diff().mean()

        # Calculate confidence based on sample size and consistency
        confidence = min(len(df) / 100, 1) * (1 - df['compound'].std())

        return {
            'overall_sentiment': weighted_sentiment,
            'sentiment_momentum': sentiment_change,
            'impact_score': total_impact,
            'confidence': confidence
        }

    def analyze_market_sentiment(self, news_list):
        """Analyze market news sentiment"""
        texts = []
        sources = []

        for news in news_list:
            if 'title' in news:
                texts.append(news['title'])
                sources.append(news.get('publisher', 'Unknown'))

        sentiment_data = self.analyze_text_sentiment(texts, sources)
        metrics = self.get_aggregated_sentiment(sentiment_data)

        return sentiment_data, metrics