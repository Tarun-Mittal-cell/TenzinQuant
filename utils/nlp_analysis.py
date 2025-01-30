import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

def analyze_news_sentiment(news_list):
    """Analyze sentiment of news articles"""
    sia = SentimentIntensityAnalyzer()
    
    sentiments = []
    for news in news_list:
        if 'title' in news:
            sentiment = sia.polarity_scores(news['title'])
            sentiments.append(sentiment['compound'])
    
    if sentiments:
        avg_sentiment = np.mean(sentiments)
        sentiment_label = get_sentiment_label(avg_sentiment)
        return avg_sentiment, sentiment_label
    return 0, "Neutral"

def get_sentiment_label(score):
    """Convert sentiment score to label"""
    if score >= 0.2:
        return "Bullish"
    elif score <= -0.2:
        return "Bearish"
    else:
        return "Neutral"

def generate_insight(metrics, sentiment_label, prediction, current_price):
    """Generate natural language insights"""
    insight = []
    
    # Price prediction insight
    price_change = ((prediction - current_price) / current_price) * 100
    direction = "increase" if price_change > 0 else "decrease"
    insight.append(f"AI models predict a {abs(price_change):.2f}% {direction} in stock price.")
    
    # Sentiment insight
    insight.append(f"Market sentiment analysis indicates a {sentiment_label} outlook.")
    
    # Volatility insight
    if 'volatility' in metrics:
        vol_level = "high" if metrics['volatility'] > 0.3 else "moderate" if metrics['volatility'] > 0.15 else "low"
        insight.append(f"Stock shows {vol_level} volatility at {metrics['volatility']:.2f}%.")
    
    return insight
