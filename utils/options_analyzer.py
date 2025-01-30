import pandas as pd
import numpy as np
from scipy.stats import norm

class OptionsAnalyzer:
    def __init__(self):
        self.risk_free_rate = 0.02  # 2% risk-free rate
        
    def calculate_option_price(self, S, K, T, r, sigma, option_type='call'):
        """
        Calculate option price using Black-Scholes model.
        
        Parameters:
        S: Current stock price
        K: Strike price
        T: Time to expiration (in years)
        r: Risk-free rate
        sigma: Volatility
        option_type: 'call' or 'put'
        """
        d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        
        if option_type == 'call':
            price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
        else:  # put
            price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
            
        return price
    
    def get_options_chain(self, symbol, current_price, expiry_date):
        """
        Generate options chain for a given stock.
        Returns a DataFrame with strike prices and option prices.
        """
        # Generate strike prices around current price
        strikes = np.linspace(current_price*0.8, current_price*1.2, 10)
        
        # Calculate time to expiration (simplified for demo)
        T = 30/365  # 30 days
        
        # Generate options chain
        chain = []
        for strike in strikes:
            # Simulate implied volatility
            iv = np.random.uniform(0.2, 0.4)
            
            # Calculate option prices
            call_price = self.calculate_option_price(current_price, strike, T, self.risk_free_rate, iv, 'call')
            put_price = self.calculate_option_price(current_price, strike, T, self.risk_free_rate, iv, 'put')
            
            chain.append({
                'Strike': strike,
                'Call Price': call_price,
                'Put Price': put_price,
                'Call IV': iv,
                'Put IV': iv,
                'Delta': self.calculate_delta(current_price, strike, T, iv),
                'Gamma': self.calculate_gamma(current_price, strike, T, iv),
                'Theta': self.calculate_theta(current_price, strike, T, iv)
            })
        
        return pd.DataFrame(chain)
    
    def calculate_delta(self, S, K, T, sigma):
        """Calculate option Delta."""
        d1 = (np.log(S/K) + (self.risk_free_rate + sigma**2/2)*T) / (sigma*np.sqrt(T))
        return norm.cdf(d1)
    
    def calculate_gamma(self, S, K, T, sigma):
        """Calculate option Gamma."""
        d1 = (np.log(S/K) + (self.risk_free_rate + sigma**2/2)*T) / (sigma*np.sqrt(T))
        return norm.pdf(d1)/(S*sigma*np.sqrt(T))
    
    def calculate_theta(self, S, K, T, sigma):
        """Calculate option Theta."""
        d1 = (np.log(S/K) + (self.risk_free_rate + sigma**2/2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        theta = -S*norm.pdf(d1)*sigma/(2*np.sqrt(T)) - self.risk_free_rate*K*np.exp(-self.risk_free_rate*T)*norm.cdf(d2)
        return theta/365  # Convert to daily theta