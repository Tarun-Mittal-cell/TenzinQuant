from typing import Dict, List, Optional
import logging
from transformers import pipeline
import numpy as np

logger = logging.getLogger(__name__)

class TenzinBot:
    """AI chatbot for trading assistance"""
    
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification")
        self.qa_pipeline = pipeline("question-answering")
        
        # Define intents and responses
        self.intents = {
            'price_prediction': {
                'patterns': ['predict', 'forecast', 'price target', 'where is the price going'],
                'responses': [
                    "Based on my analysis, {symbol}'s price might {direction} to {target} in the {timeframe}.",
                    "The AI models suggest {symbol} could {direction} by {percentage}% in the {timeframe}.",
                    "Technical indicators point to a {sentiment} outlook for {symbol}."
                ]
            },
            'market_analysis': {
                'patterns': ['analyze', 'technical analysis', 'indicators', 'what do you think about'],
                'responses': [
                    "Looking at {symbol}, the technical indicators show {analysis}.",
                    "The current market analysis for {symbol} indicates {analysis}.",
                    "Based on multiple indicators, {symbol} is showing {analysis}."
                ]
            },
            'trading_signal': {
                'patterns': ['should I buy', 'should I sell', 'good time to invest', 'trading signal'],
                'responses': [
                    "The current signal for {symbol} is {signal} with {confidence}% confidence.",
                    "Based on market conditions, the recommendation for {symbol} is to {signal}.",
                    "Technical analysis suggests a {signal} signal for {symbol}."
                ]
            },
            'portfolio_advice': {
                'patterns': ['portfolio', 'diversification', 'risk management', 'allocation'],
                'responses': [
                    "For optimal portfolio balance, consider {advice}.",
                    "To manage risk effectively, you might want to {advice}.",
                    "Based on your portfolio composition, I suggest {advice}."
                ]
            },
            'market_sentiment': {
                'patterns': ['sentiment', 'market mood', 'what are people saying', 'social media'],
                'responses': [
                    "The overall sentiment for {symbol} is {sentiment} based on recent data.",
                    "Market sentiment analysis shows {sentiment} signals for {symbol}.",
                    "Social media and news sentiment for {symbol} is trending {sentiment}."
                ]
            }
        }
    
    def get_intent(self, query: str) -> str:
        """Determine the intent of the user's query"""
        candidate_labels = list(self.intents.keys())
        result = self.classifier(query, candidate_labels)
        return result['labels'][0]
    
    def format_response(self, intent: str, context: Dict) -> str:
        """Format response based on intent and context"""
        try:
            responses = self.intents[intent]['responses']
            response_template = np.random.choice(responses)
            
            # Format response with context
            if intent == 'price_prediction':
                return response_template.format(
                    symbol=context.get('symbol', 'the stock'),
                    direction='increase' if context.get('prediction', 0) > 0 else 'decrease',
                    target=f"${context.get('target_price', 0):.2f}",
                    timeframe=context.get('timeframe', 'short term'),
                    percentage=abs(context.get('prediction', 0))
                )
            
            elif intent == 'market_analysis':
                return response_template.format(
                    symbol=context.get('symbol', 'the stock'),
                    analysis=context.get('analysis', 'mixed signals')
                )
            
            elif intent == 'trading_signal':
                return response_template.format(
                    symbol=context.get('symbol', 'the stock'),
                    signal=context.get('signal', 'HOLD'),
                    confidence=context.get('confidence', 70)
                )
            
            elif intent == 'portfolio_advice':
                return response_template.format(
                    advice=context.get('advice', 'maintain a diversified portfolio')
                )
            
            elif intent == 'market_sentiment':
                return response_template.format(
                    symbol=context.get('symbol', 'the stock'),
                    sentiment=context.get('sentiment', 'neutral')
                )
            
            return response_template
            
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return "I apologize, but I'm having trouble processing that request. Could you please rephrase it?"
    
    def get_response(self, query: str, market_data: Optional[Dict] = None) -> str:
        """Generate response to user query"""
        try:
            # Determine intent
            intent = self.get_intent(query)
            
            # Prepare context based on market data
            context = self._prepare_context(intent, market_data) if market_data else {}
            
            # Format and return response
            return self.format_response(intent, context)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble understanding. Could you please rephrase your question?"
    
    def _prepare_context(self, intent: str, market_data: Dict) -> Dict:
        """Prepare context for response based on market data"""
        context = {}
        
        if not market_data:
            return context
        
        # Get the first symbol's data as default
        symbol = list(market_data.keys())[0]
        data = market_data[symbol]
        
        if intent == 'price_prediction':
            context = {
                'symbol': symbol,
                'prediction': float(data['change'].strip('%')),
                'target_price': data['price'] * (1 + float(data['change'].strip('%')) / 100),
                'timeframe': 'short term'
            }
        
        elif intent == 'market_analysis':
            analysis = []
            if float(data['rsi']) > 70:
                analysis.append('overbought conditions')
            elif float(data['rsi']) < 30:
                analysis.append('oversold conditions')
            if data['macd'] > 0:
                analysis.append('positive momentum')
            else:
                analysis.append('negative momentum')
                
            context = {
                'symbol': symbol,
                'analysis': ' and '.join(analysis) or 'mixed signals'
            }
        
        elif intent == 'trading_signal':
            context = {
                'symbol': symbol,
                'signal': data['signal'],
                'confidence': float(data.get('confidence', '70%').strip('%'))
            }
        
        elif intent == 'market_sentiment':
            # Determine sentiment based on technical indicators
            if data['signal'] == 'Buy' and float(data['rsi']) < 70:
                sentiment = 'bullish'
            elif data['signal'] == 'Sell' and float(data['rsi']) > 30:
                sentiment = 'bearish'
            else:
                sentiment = 'neutral'
                
            context = {
                'symbol': symbol,
                'sentiment': sentiment
            }
        
        return context