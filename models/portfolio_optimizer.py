import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.covariance import LedoitWolf

class PortfolioOptimizer:
    def __init__(self, risk_free_rate=0.02):
        self.risk_free_rate = risk_free_rate
        self.covariance_estimator = LedoitWolf()
        
    def optimize_portfolio(self, returns, risk_tolerance=0.5, esg_scores=None):
        """
        Optimize portfolio weights using Modern Portfolio Theory with ESG constraints
        
        Parameters:
        returns: DataFrame of asset returns
        risk_tolerance: float between 0 and 1 (higher means more risk-tolerant)
        esg_scores: dict of ESG scores for each asset
        """
        n_assets = returns.shape[1]
        
        # Calculate expected returns and covariance
        exp_returns = returns.mean()
        covariance = self.covariance_estimator.fit(returns).covariance_
        
        # Define optimization objective (Sharpe Ratio)
        def objective(weights):
            portfolio_return = np.sum(exp_returns * weights) * 252
            portfolio_std = np.sqrt(np.dot(weights.T, np.dot(covariance, weights))) * np.sqrt(252)
            sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_std
            return -sharpe_ratio  # Minimize negative Sharpe Ratio
        
        # Constraints
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # Weights sum to 1
        ]
        
        # Add ESG constraints if scores are provided
        if esg_scores is not None:
            min_esg_score = 70  # Minimum acceptable ESG score
            esg_constraint = {
                'type': 'ineq',
                'fun': lambda x: np.sum([x[i] * esg_scores[asset] for i, asset in enumerate(returns.columns)]) - min_esg_score
            }
            constraints.append(esg_constraint)
        
        # Bounds for weights (0 to 1)
        bounds = tuple((0, 1) for _ in range(n_assets))
        
        # Initial guess (equal weights)
        initial_weights = np.array([1/n_assets] * n_assets)
        
        # Optimize
        result = minimize(
            objective,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        # Calculate portfolio metrics
        optimal_weights = result.x
        portfolio_return = np.sum(exp_returns * optimal_weights) * 252
        portfolio_std = np.sqrt(np.dot(optimal_weights.T, np.dot(covariance, optimal_weights))) * np.sqrt(252)
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_std
        
        return {
            'weights': dict(zip(returns.columns, optimal_weights)),
            'expected_return': portfolio_return,
            'volatility': portfolio_std,
            'sharpe_ratio': sharpe_ratio
        }
    
    def calculate_risk_metrics(self, returns, weights):
        """Calculate various risk metrics for the portfolio"""
        portfolio_returns = returns.dot(weights)
        
        metrics = {
            'volatility': portfolio_returns.std() * np.sqrt(252),
            'var_95': np.percentile(portfolio_returns, 5),
            'cvar_95': portfolio_returns[portfolio_returns <= np.percentile(portfolio_returns, 5)].mean(),
            'max_drawdown': self._calculate_max_drawdown(portfolio_returns),
            'beta': self._calculate_beta(portfolio_returns, returns),
            'tracking_error': self._calculate_tracking_error(portfolio_returns, returns)
        }
        
        return metrics
    
    def _calculate_max_drawdown(self, returns):
        """Calculate maximum drawdown"""
        cum_returns = (1 + returns).cumprod()
        rolling_max = cum_returns.expanding().max()
        drawdowns = cum_returns / rolling_max - 1
        return drawdowns.min()
    
    def _calculate_beta(self, portfolio_returns, asset_returns, market_col='SPY'):
        """Calculate portfolio beta relative to market"""
        if market_col in asset_returns.columns:
            market_returns = asset_returns[market_col]
            covariance = np.cov(portfolio_returns, market_returns)[0,1]
            market_variance = np.var(market_returns)
            return covariance / market_variance
        return None
    
    def _calculate_tracking_error(self, portfolio_returns, asset_returns, benchmark_col='SPY'):
        """Calculate tracking error relative to benchmark"""
        if benchmark_col in asset_returns.columns:
            tracking_diff = portfolio_returns - asset_returns[benchmark_col]
            return tracking_diff.std() * np.sqrt(252)
        return None
    
    def generate_efficient_frontier(self, returns, n_points=50):
        """Generate efficient frontier points"""
        n_assets = returns.shape[1]
        exp_returns = returns.mean()
        covariance = self.covariance_estimator.fit(returns).covariance_
        
        # Function to minimize portfolio variance
        def portfolio_variance(weights):
            return np.dot(weights.T, np.dot(covariance, weights))
        
        # Function to calculate portfolio return
        def portfolio_return(weights):
            return np.sum(exp_returns * weights)
        
        # Generate frontier points
        target_returns = np.linspace(exp_returns.min(), exp_returns.max(), n_points)
        efficient_frontier = []
        
        for target in target_returns:
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: portfolio_return(x) - target}
            ]
            bounds = tuple((0, 1) for _ in range(n_assets))
            initial_weights = np.array([1/n_assets] * n_assets)
            
            result = minimize(
                portfolio_variance,
                initial_weights,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            if result.success:
                efficient_frontier.append({
                    'return': target * 252,
                    'volatility': np.sqrt(portfolio_variance(result.x)) * np.sqrt(252),
                    'weights': dict(zip(returns.columns, result.x))
                })
        
        return efficient_frontier