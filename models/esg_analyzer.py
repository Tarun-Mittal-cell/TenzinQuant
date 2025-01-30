import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from transformers import pipeline

class ESGAnalyzer:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        
        # Pre-defined ESG criteria weights
        self.criteria_weights = {
            'environmental': {
                'carbon_emissions': 0.3,
                'renewable_energy': 0.2,
                'waste_management': 0.2,
                'water_usage': 0.15,
                'biodiversity': 0.15
            },
            'social': {
                'employee_satisfaction': 0.25,
                'diversity_inclusion': 0.25,
                'community_relations': 0.2,
                'human_rights': 0.15,
                'health_safety': 0.15
            },
            'governance': {
                'board_independence': 0.3,
                'shareholder_rights': 0.2,
                'executive_compensation': 0.2,
                'business_ethics': 0.15,
                'transparency': 0.15
            }
        }
    
    def calculate_esg_score(self, company_data):
        """
        Calculate ESG score based on company data and predefined criteria
        
        Parameters:
        company_data: dict containing ESG metrics for each criteria
        """
        scores = {
            'environmental': self._calculate_component_score(company_data, 'environmental'),
            'social': self._calculate_component_score(company_data, 'social'),
            'governance': self._calculate_component_score(company_data, 'governance')
        }
        
        # Calculate total ESG score (weighted average)
        total_score = (
            0.4 * scores['environmental'] +
            0.3 * scores['social'] +
            0.3 * scores['governance']
        )
        
        return {
            'total_score': total_score,
            'component_scores': scores
        }
    
    def _calculate_component_score(self, data, component):
        """Calculate score for a specific ESG component"""
        weights = self.criteria_weights[component]
        score = 0
        
        for criterion, weight in weights.items():
            if criterion in data:
                score += weight * data[criterion]
        
        return score
    
    def analyze_sustainability_reports(self, text_data):
        """
        Analyze sustainability reports using NLP
        
        Parameters:
        text_data: str or list of str containing sustainability report text
        """
        if isinstance(text_data, str):
            text_data = [text_data]
        
        # Analyze sentiment of sustainability statements
        sentiments = self.sentiment_analyzer(text_data)
        
        # Extract key metrics and commitments
        metrics = self._extract_sustainability_metrics(text_data)
        
        return {
            'sentiment': np.mean([s['score'] if s['label'] == 'POSITIVE' else -s['score'] for s in sentiments]),
            'metrics': metrics
        }
    
    def _extract_sustainability_metrics(self, texts):
        """Extract key sustainability metrics from text using regex patterns"""
        # Implement metric extraction logic here
        # This is a placeholder implementation
        metrics = {
            'carbon_reduction_targets': [],
            'renewable_energy_goals': [],
            'diversity_targets': [],
            'governance_policies': []
        }
        return metrics
    
    def calculate_portfolio_esg_impact(self, portfolio, company_scores):
        """
        Calculate ESG impact of a portfolio
        
        Parameters:
        portfolio: dict of {symbol: weight}
        company_scores: dict of {symbol: esg_score}
        """
        total_score = 0
        impact_areas = {
            'carbon_footprint': 0,
            'social_impact': 0,
            'governance_quality': 0
        }
        
        for symbol, weight in portfolio.items():
            if symbol in company_scores:
                score = company_scores[symbol]
                total_score += weight * score['total_score']
                
                # Calculate impact areas
                impact_areas['carbon_footprint'] += weight * score['component_scores']['environmental']
                impact_areas['social_impact'] += weight * score['component_scores']['social']
                impact_areas['governance_quality'] += weight * score['component_scores']['governance']
        
        return {
            'total_score': total_score,
            'impact_areas': impact_areas
        }
    
    def generate_esg_report(self, company, scores, analysis):
        """Generate comprehensive ESG report"""
        report = {
            'company': company,
            'summary': {
                'total_score': scores['total_score'],
                'environmental_score': scores['component_scores']['environmental'],
                'social_score': scores['component_scores']['social'],
                'governance_score': scores['component_scores']['governance']
            },
            'strengths': self._identify_strengths(scores),
            'weaknesses': self._identify_weaknesses(scores),
            'recommendations': self._generate_recommendations(scores),
            'sentiment_analysis': analysis['sentiment'],
            'key_metrics': analysis['metrics']
        }
        
        return report
    
    def _identify_strengths(self, scores):
        """Identify areas where the company excels"""
        strengths = []
        threshold = 80  # Score threshold for strength
        
        for component, score in scores['component_scores'].items():
            if score >= threshold:
                strengths.append(f"Strong performance in {component} with score {score:.1f}")
        
        return strengths
    
    def _identify_weaknesses(self, scores):
        """Identify areas needing improvement"""
        weaknesses = []
        threshold = 60  # Score threshold for weakness
        
        for component, score in scores['component_scores'].items():
            if score < threshold:
                weaknesses.append(f"Needs improvement in {component} with score {score:.1f}")
        
        return weaknesses
    
    def _generate_recommendations(self, scores):
        """Generate improvement recommendations based on scores"""
        recommendations = []
        
        # Example recommendation logic
        if scores['component_scores']['environmental'] < 70:
            recommendations.append("Implement stronger environmental policies and carbon reduction targets")
        if scores['component_scores']['social'] < 70:
            recommendations.append("Enhance diversity and inclusion initiatives")
        if scores['component_scores']['governance'] < 70:
            recommendations.append("Improve board independence and shareholder rights")
        
        return recommendations