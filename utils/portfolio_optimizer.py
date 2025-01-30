import numpy as np
import pandas as pd
from scipy.optimize import minimize
import yfinance as yf

class PortfolioOptimizer:
    def __init__(self, symbols, start_date=None, end_date=None):
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date
        self.returns = None
        self.mean_returns = None
        self.cov_matrix = None

    def fetch_data(self):
        """Fetch historical data for all symbols"""
        data = pd.DataFrame()
        for symbol in self.symbols:
            stock = yf.Ticker(symbol)
            hist = stock.history(period='1y')['Close']
            data[symbol] = hist

        # Calculate daily returns
        self.returns = data.pct_change()
        self.mean_returns = self.returns.mean()
        self.cov_matrix = self.returns.cov()

        return self.returns

    def portfolio_performance(self, weights):
        """Calculate portfolio performance metrics"""
        returns = np.sum(self.mean_returns * weights) * 252  # Annualized returns
        risk = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix * 252, weights)))
        sharpe_ratio = returns / risk  # Assuming risk-free rate = 0
        return returns, risk, sharpe_ratio

    def optimize_portfolio(self):
        """Find the optimal portfolio weights"""
        num_assets = len(self.symbols)
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}  # weights sum to 1
        ]
        bounds = tuple((0, 1) for _ in range(num_assets))  # weights between 0 and 1

        # Initial guess (equal weights)
        init_weights = np.array([1/num_assets] * num_assets)

        # Optimize for Sharpe Ratio
        def objective(weights):
            return -self.portfolio_performance(weights)[2]  # Negative for minimization

        result = minimize(objective, init_weights, method='SLSQP',
                         bounds=bounds, constraints=constraints)

        return result.x

    def efficient_frontier(self, num_portfolios=100):
        """Generate efficient frontier points"""
        returns_range = np.linspace(self.mean_returns.min(), self.mean_returns.max(), num_portfolios)
        efficient_portfolios = []
        num_assets = len(self.symbols)

        for ret in returns_range:
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: np.sum(self.mean_returns * x) * 252 - ret}
            ]
            bounds = tuple((0, 1) for _ in range(num_assets))

            result = minimize(lambda x: np.sqrt(np.dot(x.T, np.dot(self.cov_matrix * 252, x))),
                            np.array([1/num_assets] * num_assets),
                            method='SLSQP',
                            bounds=bounds,
                            constraints=constraints)

            if result.success:
                risk = np.sqrt(np.dot(result.x.T, np.dot(self.cov_matrix * 252, result.x)))
                efficient_portfolios.append({
                    'expected_return': ret,
                    'volatility': risk,
                    'weights': result.x
                })

        return pd.DataFrame(efficient_portfolios)

    def get_optimal_portfolio(self):
        """Get the optimal portfolio allocation"""
        if self.returns is None:
            self.fetch_data()

        optimal_weights = self.optimize_portfolio()
        returns, risk, sharpe = self.portfolio_performance(optimal_weights)

        return {
            'weights': dict(zip(self.symbols, optimal_weights)),
            'expected_annual_return': returns,
            'annual_volatility': risk,
            'sharpe_ratio': sharpe
        }