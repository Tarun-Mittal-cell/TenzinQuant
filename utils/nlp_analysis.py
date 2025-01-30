import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
from datetime import datetime, timedelta

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

def analyze_news_sentiment(news_list):
    """Analyze sentiment of news articles with enhanced metrics"""
    sia = SentimentIntensityAnalyzer()

    detailed_sentiments = []
    for news in news_list:
        if 'title' in news:
            sentiment_scores = sia.polarity_scores(news['title'])
            timestamp = news.get('providerPublishTime', datetime.now().timestamp())
            source = news.get('publisher', 'Unknown')

            detailed_sentiments.append({
                'compound': sentiment_scores['compound'],
                'positive': sentiment_scores['pos'],
                'negative': sentiment_scores['neg'],
                'neutral': sentiment_scores['neu'],
                'timestamp': timestamp,
                'source': source
            })

    if detailed_sentiments:
        avg_sentiment = np.mean([s['compound'] for s in detailed_sentiments])
        sentiment_label = get_sentiment_label(avg_sentiment)
        return avg_sentiment, sentiment_label, detailed_sentiments
    return 0, "Neutral", []

def get_sentiment_label(score):
    """Convert sentiment score to detailed label"""
    if score >= 0.5:
        return "Strongly Bullish"
    elif score >= 0.2:
        return "Moderately Bullish"
    elif score > -0.2:
        return "Neutral"
    elif score > -0.5:
        return "Moderately Bearish"
    else:
        return "Strongly Bearish"

def calculate_source_credibility(source, sentiment_history):
    """Calculate source credibility based on sentiment consistency"""
    source_sentiments = [s['compound'] for s in sentiment_history if s['source'] == source]
    if len(source_sentiments) < 2:
        return 0.5  # Default credibility for new sources

    consistency = 1 - np.std(source_sentiments)  # Higher consistency = lower standard deviation
    return min(max(consistency, 0), 1)  # Normalize between 0 and 1

def generate_insight(metrics, sentiment_label, prediction, current_price, detailed_sentiments=None):
    """Generate enhanced natural language insights"""
    insights = []

    # Price prediction insight
    price_change = ((prediction - current_price) / current_price) * 100
    direction = "increase" if price_change > 0 else "decrease"
    insights.append(f"AI models predict a {abs(price_change):.2f}% {direction} in stock price.")

    # Enhanced sentiment insights
    insights.append(f"Market sentiment analysis indicates a {sentiment_label} outlook.")

    if detailed_sentiments:
        # Recent sentiment trend
        recent_sentiment = np.mean([s['compound'] for s in detailed_sentiments[-3:]])
        trend = "improving" if recent_sentiment > 0 else "declining"
        insights.append(f"Recent news sentiment is {trend} with {abs(recent_sentiment):.2f} strength.")

        # Source analysis
        sources = set(s['source'] for s in detailed_sentiments)
        for source in sources:
            credibility = calculate_source_credibility(source, detailed_sentiments)
            if credibility > 0.7:
                insights.append(f"{source} shows high credibility with consistent sentiment reporting.")

    # Volatility insight
    if 'volatility' in metrics:
        vol_level = "high" if metrics['volatility'] > 0.3 else "moderate" if metrics['volatility'] > 0.15 else "low"
        insights.append(f"Stock shows {vol_level} volatility at {metrics['volatility']:.2f}%.")

    return insights