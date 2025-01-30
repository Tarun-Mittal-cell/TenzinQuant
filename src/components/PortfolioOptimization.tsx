import React, { useState } from 'react'
import { portfolioOptimizer } from '../services/portfolio-optimizer-simple'

const samplePositions = [
  {
    symbol: 'AAPL',
    shares: 100,
    currentPrice: 150,
    volatility: 0.25,
    beta: 1.2
  },
  {
    symbol: 'GOOGL',
    shares: 50,
    currentPrice: 2800,
    volatility: 0.28,
    beta: 1.1
  },
  {
    symbol: 'MSFT',
    shares: 200,
    currentPrice: 300,
    volatility: 0.22,
    beta: 1.0
  }
]

export function PortfolioOptimization() {
  const [riskTolerance, setRiskTolerance] = useState(0.5)
  const [optimization, setOptimization] = useState(
    portfolioOptimizer.optimizePortfolio(samplePositions, 0.5)
  )
  const [metrics, setMetrics] = useState(
    portfolioOptimizer.calculateRiskMetrics(samplePositions)
  )

  const handleOptimize = (newRiskTolerance: number) => {
    setRiskTolerance(newRiskTolerance)
    const result = portfolioOptimizer.optimizePortfolio(samplePositions, newRiskTolerance)
    setOptimization(result)
  }

  return (
    <div className="space-y-6 p-6 bg-quantum-dark-200 rounded-lg">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-bold text-quantum-light-100">
          Portfolio Optimization
        </h2>
        <div className="flex items-center space-x-4">
          <span className="text-quantum-light-300">Risk Tolerance</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={riskTolerance}
            onChange={(e) => handleOptimize(parseFloat(e.target.value))}
            className="w-32"
          />
          <span className="text-quantum-light-100 w-12">
            {(riskTolerance * 100).toFixed(0)}%
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Optimization Results */}
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-quantum-light-100">
            Optimized Allocations
          </h3>
          <div className="space-y-2">
            {Object.entries(optimization.allocations).map(([symbol, allocation]) => (
              <div
                key={symbol}
                className="flex justify-between items-center p-3 bg-quantum-dark-300 rounded"
              >
                <span className="text-quantum-light-100">{symbol}</span>
                <div className="flex items-center space-x-2">
                  <div className="w-32 h-2 bg-quantum-dark-400 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-quantum-primary"
                      style={{ width: `${allocation * 100}%` }}
                    />
                  </div>
                  <span className="text-quantum-light-300 w-16 text-right">
                    {(allocation * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Metrics */}
        <div className="space-y-4">
          <h3 className="text-lg font-medium text-quantum-light-100">
            Portfolio Metrics
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-quantum-dark-300 rounded">
              <div className="text-sm text-quantum-light-300">Expected Return</div>
              <div className="text-xl font-bold text-quantum-primary">
                {(optimization.expectedReturn * 100).toFixed(1)}%
              </div>
            </div>
            <div className="p-4 bg-quantum-dark-300 rounded">
              <div className="text-sm text-quantum-light-300">Risk</div>
              <div className="text-xl font-bold text-quantum-accent">
                {(optimization.risk * 100).toFixed(1)}%
              </div>
            </div>
            <div className="p-4 bg-quantum-dark-300 rounded">
              <div className="text-sm text-quantum-light-300">Sharpe Ratio</div>
              <div className="text-xl font-bold text-quantum-light-100">
                {optimization.sharpeRatio.toFixed(2)}
              </div>
            </div>
            <div className="p-4 bg-quantum-dark-300 rounded">
              <div className="text-sm text-quantum-light-300">Beta</div>
              <div className="text-xl font-bold text-quantum-light-100">
                {metrics.beta.toFixed(2)}
              </div>
            </div>
          </div>

          <div className="mt-4">
            <div className="text-sm text-quantum-light-300 mb-2">Risk Score</div>
            <div className="h-4 bg-quantum-dark-400 rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-quantum-primary to-quantum-accent"
                style={{ width: `${metrics.riskScore}%` }}
              />
            </div>
            <div className="text-right text-sm text-quantum-light-300 mt-1">
              {metrics.riskScore.toFixed(0)}/100
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}