/**
 * Simple Portfolio Optimizer Service
 * Focuses on core functionality with minimal dependencies
 */

interface Position {
  symbol: string
  shares: number
  currentPrice: number
  volatility: number
  beta: number
}

interface OptimizationResult {
  allocations: { [symbol: string]: number }
  expectedReturn: number
  risk: number
  sharpeRatio: number
}

class PortfolioOptimizer {
  private riskFreeRate = 0.02 // 2% risk-free rate

  /**
   * Optimize portfolio using Modern Portfolio Theory
   */
  optimizePortfolio(positions: Position[], riskTolerance: number): OptimizationResult {
    // Calculate portfolio metrics
    const totalValue = positions.reduce((sum, pos) => sum + pos.shares * pos.currentPrice, 0)
    const weights = positions.map(pos => (pos.shares * pos.currentPrice) / totalValue)
    
    // Calculate expected returns (simplified)
    const expectedReturns = positions.map(pos => {
      const marketReturn = 0.08 // Assumed market return of 8%
      return this.riskFreeRate + pos.beta * (marketReturn - this.riskFreeRate)
    })

    // Calculate portfolio expected return
    const portfolioReturn = weights.reduce((sum, weight, i) => 
      sum + weight * expectedReturns[i], 0)

    // Calculate portfolio risk (simplified using volatilities)
    const portfolioRisk = Math.sqrt(
      weights.reduce((sum, weight, i) => 
        sum + Math.pow(weight * positions[i].volatility, 2), 0)
    )

    // Calculate Sharpe ratio
    const sharpeRatio = (portfolioReturn - this.riskFreeRate) / portfolioRisk

    // Create optimized allocations based on risk tolerance
    const optimizedAllocations: { [symbol: string]: number } = {}
    positions.forEach((pos, i) => {
      // Adjust weights based on risk tolerance and Sharpe ratio
      const adjustedWeight = weights[i] * (1 + (sharpeRatio - 1) * riskTolerance)
      optimizedAllocations[pos.symbol] = adjustedWeight
    })

    // Normalize allocations to sum to 1
    const totalAllocation = Object.values(optimizedAllocations).reduce((a, b) => a + b, 0)
    Object.keys(optimizedAllocations).forEach(symbol => {
      optimizedAllocations[symbol] /= totalAllocation
    })

    return {
      allocations: optimizedAllocations,
      expectedReturn: portfolioReturn,
      risk: portfolioRisk,
      sharpeRatio
    }
  }

  /**
   * Get rebalancing recommendations
   */
  getRebalancingRecommendations(
    currentAllocations: { [symbol: string]: number },
    targetAllocations: { [symbol: string]: number },
    threshold = 0.05 // 5% threshold
  ) {
    const recommendations = []

    for (const symbol in targetAllocations) {
      const currentAllocation = currentAllocations[symbol] || 0
      const targetAllocation = targetAllocations[symbol]
      const difference = targetAllocation - currentAllocation

      if (Math.abs(difference) > threshold) {
        recommendations.push({
          symbol,
          action: difference > 0 ? 'BUY' : 'SELL',
          amount: Math.abs(difference),
          reason: `Rebalance to target allocation of ${(targetAllocation * 100).toFixed(1)}%`
        })
      }
    }

    return recommendations
  }

  /**
   * Calculate risk metrics
   */
  calculateRiskMetrics(positions: Position[]) {
    const totalValue = positions.reduce((sum, pos) => sum + pos.shares * pos.currentPrice, 0)
    const weights = positions.map(pos => (pos.shares * pos.currentPrice) / totalValue)

    // Portfolio beta
    const portfolioBeta = weights.reduce((sum, weight, i) => 
      sum + weight * positions[i].beta, 0)

    // Portfolio volatility
    const portfolioVolatility = Math.sqrt(
      weights.reduce((sum, weight, i) => 
        sum + Math.pow(weight * positions[i].volatility, 2), 0)
    )

    // Value at Risk (VaR) - 95% confidence
    const valueAtRisk = totalValue * portfolioVolatility * 1.645

    return {
      beta: portfolioBeta,
      volatility: portfolioVolatility,
      valueAtRisk,
      riskScore: this.calculateRiskScore(portfolioBeta, portfolioVolatility)
    }
  }

  /**
   * Calculate risk score (0-100)
   */
  private calculateRiskScore(beta: number, volatility: number): number {
    const betaScore = (beta / 2) * 50 // Beta of 2 = max score of 50
    const volScore = (volatility / 0.5) * 50 // Volatility of 50% = max score of 50
    return Math.min(Math.max(betaScore + volScore, 0), 100)
  }
}

export const portfolioOptimizer = new PortfolioOptimizer()