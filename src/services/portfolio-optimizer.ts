import { create } from 'zustand'
import { PortfolioAnalytics, RiskMetrics, PortfolioPosition } from '@/types'

interface OptimizationState {
  portfolio: PortfolioAnalytics | null
  isOptimizing: boolean
  optimizationProgress: number
  optimizePortfolio: (positions: PortfolioPosition[], riskTolerance: number) => Promise<void>
  calculateRiskMetrics: (positions: PortfolioPosition[]) => RiskMetrics
  getRecommendations: () => void
}

export const usePortfolioStore = create<OptimizationState>((set, get) => ({
  portfolio: null,
  isOptimizing: false,
  optimizationProgress: 0,

  optimizePortfolio: async (positions: PortfolioPosition[], riskTolerance: number) => {
    set({ isOptimizing: true, optimizationProgress: 0 })

    try {
      // Simulate optimization steps
      for (let i = 0; i <= 10; i++) {
        await new Promise(resolve => setTimeout(resolve, 500))
        set({ optimizationProgress: i * 10 })

        // Portfolio optimization logic
        const optimizedPortfolio: PortfolioAnalytics = {
          totalValue: positions.reduce((sum, pos) => sum + pos.currentValue, 0),
          cashBalance: 100000, // Example cash balance
          positions: positions.map(pos => ({
            ...pos,
            weight: pos.currentValue / positions.reduce((sum, p) => sum + p.currentValue, 0),
            riskScore: Math.random() * 100, // Calculate actual risk score
          })),
          performance: {
            daily: Math.random() * 0.02 - 0.01,
            weekly: Math.random() * 0.05 - 0.025,
            monthly: Math.random() * 0.1 - 0.05,
            yearly: Math.random() * 0.2 - 0.1,
          },
          riskMetrics: get().calculateRiskMetrics(positions),
          diversification: {
            sectorWeights: {
              'Technology': 0.3,
              'Healthcare': 0.2,
              'Finance': 0.15,
              'Consumer': 0.15,
              'Energy': 0.1,
              'Other': 0.1,
            },
            geographicWeights: {
              'North America': 0.6,
              'Europe': 0.2,
              'Asia': 0.15,
              'Other': 0.05,
            },
            assetClassWeights: {
              'Stocks': 0.7,
              'Bonds': 0.2,
              'Cash': 0.1,
            },
          },
          recommendations: [
            {
              type: 'REBALANCE',
              symbol: 'AAPL',
              reason: 'Portfolio overweight in technology sector',
              impact: 0.05,
              confidence: 0.85,
            },
            {
              type: 'BUY',
              symbol: 'XLV',
              reason: 'Increase healthcare exposure for better diversification',
              impact: 0.03,
              confidence: 0.78,
            },
          ],
        }

        set({ portfolio: optimizedPortfolio })
      }
    } catch (error) {
      console.error('Portfolio optimization error:', error)
    } finally {
      set({ isOptimizing: false, optimizationProgress: 100 })
    }
  },

  calculateRiskMetrics: (positions: PortfolioPosition[]): RiskMetrics => {
    // Calculate Value at Risk (VaR)
    const returns = positions.map(pos => pos.performance.daily)
    const portfolioReturn = returns.reduce((sum, ret, i) => 
      sum + ret * positions[i].weight, 0)
    const portfolioStd = Math.sqrt(
      returns.reduce((sum, ret, i) => 
        sum + Math.pow(ret - portfolioReturn, 2) * positions[i].weight, 0)
    )

    // Calculate correlations
    const correlations: Record<string, number> = {}
    positions.forEach((pos1, i) => {
      positions.forEach((pos2, j) => {
        if (i < j) {
          const correlation = calculateCorrelation(
            [pos1.performance.daily, pos1.performance.weekly, pos1.performance.monthly],
            [pos2.performance.daily, pos2.performance.weekly, pos2.performance.monthly]
          )
          correlations[`${pos1.symbol}-${pos2.symbol}`] = correlation
        }
      })
    })

    return {
      var: portfolioStd * 1.645 * Math.sqrt(252), // 95% VaR, annualized
      beta: 1.1, // Example beta
      alpha: 0.02, // Example alpha
      sharpeRatio: (portfolioReturn - 0.02) / portfolioStd, // Risk-free rate = 2%
      sortinoRatio: calculateSortinoRatio(returns),
      maxDrawdown: calculateMaxDrawdown(returns),
      correlations,
    }
  },

  getRecommendations: () => {
    const portfolio = get().portfolio
    if (!portfolio) return

    // Implement recommendation logic based on portfolio analysis
    // This would include position sizing, rebalancing, and new investment suggestions
  },
}))

// Helper functions
function calculateCorrelation(x: number[], y: number[]): number {
  const n = x.length
  const sum_x = x.reduce((a, b) => a + b, 0)
  const sum_y = y.reduce((a, b) => a + b, 0)
  const sum_xy = x.reduce((sum, xi, i) => sum + xi * y[i], 0)
  const sum_x2 = x.reduce((sum, xi) => sum + xi * xi, 0)
  const sum_y2 = y.reduce((sum, yi) => sum + yi * yi, 0)

  const numerator = n * sum_xy - sum_x * sum_y
  const denominator = Math.sqrt(
    (n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)
  )

  return numerator / denominator
}

function calculateSortinoRatio(returns: number[]): number {
  const targetReturn = 0
  const downside = returns.filter(r => r < targetReturn)
  const downsideStd = Math.sqrt(
    downside.reduce((sum, r) => sum + Math.pow(r - targetReturn, 2), 0) / 
    downside.length
  )
  const avgReturn = returns.reduce((sum, r) => sum + r, 0) / returns.length
  return (avgReturn - targetReturn) / downsideStd
}

function calculateMaxDrawdown(returns: number[]): number {
  let maxDrawdown = 0
  let peak = -Infinity
  let value = 1

  returns.forEach(ret => {
    value *= (1 + ret)
    if (value > peak) {
      peak = value
    }
    const drawdown = (peak - value) / peak
    if (drawdown > maxDrawdown) {
      maxDrawdown = drawdown
    }
  })

  return maxDrawdown
}