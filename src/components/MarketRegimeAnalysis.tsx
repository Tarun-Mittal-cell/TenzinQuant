import { motion } from 'framer-motion'
import { useQuantumStore } from '@/services/quantum-predictor'
import { formatPercentage } from '@/utils/format'
import { Card } from '@tremor/react'
import { 
  Brain, 
  TrendingUp, 
  TrendingDown, 
  Activity,
  Minimize2,
  RefreshCw,
  Zap,
  Scale
} from 'lucide-react'
import { useEffect } from 'react'

const regimeIcons = {
  'BULLISH_TREND': TrendingUp,
  'BEARISH_TREND': TrendingDown,
  'HIGH_VOLATILITY': Activity,
  'LOW_VOLATILITY': Minimize2,
  'MEAN_REVERTING': RefreshCw,
  'MOMENTUM': Zap,
  'NEUTRAL': Scale,
} as const

const regimeDescriptions = {
  'BULLISH_TREND': 'Market showing strong upward momentum with positive sentiment',
  'BEARISH_TREND': 'Market experiencing sustained downward pressure',
  'HIGH_VOLATILITY': 'Increased market uncertainty and price swings',
  'LOW_VOLATILITY': 'Stable market conditions with minimal price fluctuations',
  'MEAN_REVERTING': 'Prices tend to move back toward historical average',
  'MOMENTUM': 'Strong directional movement in asset prices',
  'NEUTRAL': 'Balanced market conditions without clear directional bias',
} as const

const regimeStrategies = {
  'BULLISH_TREND': [
    'Focus on growth stocks and momentum plays',
    'Consider leveraged long positions',
    'Look for breakout opportunities'
  ],
  'BEARISH_TREND': [
    'Increase defensive positions',
    'Consider short positions or hedging',
    'Focus on value stocks with strong fundamentals'
  ],
  'HIGH_VOLATILITY': [
    'Implement options strategies',
    'Reduce position sizes',
    'Focus on risk management'
  ],
  'LOW_VOLATILITY': [
    'Consider yield-generating strategies',
    'Look for mean reversion opportunities',
    'Focus on carry trades'
  ],
  'MEAN_REVERTING': [
    'Look for overbought/oversold conditions',
    'Implement mean reversion strategies',
    'Focus on pairs trading'
  ],
  'MOMENTUM': [
    'Follow trend-following strategies',
    'Focus on relative strength',
    'Look for continuation patterns'
  ],
  'NEUTRAL': [
    'Focus on market-neutral strategies',
    'Consider arbitrage opportunities',
    'Emphasize diversification'
  ],
} as const

export function MarketRegimeAnalysis() {
  const { marketRegime, confidence, analyzeMarketRegime } = useQuantumStore()
  
  useEffect(() => {
    analyzeMarketRegime()
    const interval = setInterval(analyzeMarketRegime, 60000) // Update every minute
    return () => clearInterval(interval)
  }, [analyzeMarketRegime])

  const RegimeIcon = regimeIcons[marketRegime]

  return (
    <Card className="bg-quantum-dark-200 p-6">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Brain className="w-6 h-6 text-quantum-primary" />
            <h2 className="text-xl font-bold text-quantum-light-100">
              Market Regime Analysis
            </h2>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-quantum-light-300">
              Confidence: {formatPercentage(confidence.quantum)}
            </span>
            <motion.div
              className="flex-1 w-20 h-2 bg-quantum-dark-300 rounded-full overflow-hidden"
            >
              <motion.div
                className="h-full bg-quantum-primary"
                initial={{ width: 0 }}
                animate={{ width: `${confidence.quantum * 100}%` }}
                transition={{ duration: 0.5 }}
              />
            </motion.div>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <div className="flex-shrink-0">
            <motion.div
              className="p-4 bg-quantum-dark-300 rounded-lg"
              animate={{
                scale: [1, 1.05, 1],
                rotate: [0, 5, -5, 0]
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                repeatType: "reverse"
              }}
            >
              <RegimeIcon className="w-8 h-8 text-quantum-primary" />
            </motion.div>
          </div>
          <div>
            <h3 className="text-lg font-bold text-quantum-light-100">
              {marketRegime.replace('_', ' ')}
            </h3>
            <p className="text-quantum-light-300">
              {regimeDescriptions[marketRegime]}
            </p>
          </div>
        </div>

        <div className="space-y-4">
          <h4 className="font-medium text-quantum-light-100">
            Recommended Strategies
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {regimeStrategies[marketRegime].map((strategy, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-start space-x-3 p-3 bg-quantum-dark-300 rounded-lg"
              >
                <div className="flex-shrink-0 mt-1">
                  <div className="w-2 h-2 rounded-full bg-quantum-primary" />
                </div>
                <p className="text-sm text-quantum-light-300">{strategy}</p>
              </motion.div>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-3 bg-quantum-dark-300 rounded-lg">
            <p className="text-sm text-quantum-light-300">Technical</p>
            <p className="text-lg font-bold text-quantum-light-100">
              {formatPercentage(confidence.technical)}
            </p>
          </div>
          <div className="p-3 bg-quantum-dark-300 rounded-lg">
            <p className="text-sm text-quantum-light-300">Fundamental</p>
            <p className="text-lg font-bold text-quantum-light-100">
              {formatPercentage(confidence.fundamental)}
            </p>
          </div>
          <div className="p-3 bg-quantum-dark-300 rounded-lg">
            <p className="text-sm text-quantum-light-300">Sentiment</p>
            <p className="text-lg font-bold text-quantum-light-100">
              {formatPercentage(confidence.sentiment)}
            </p>
          </div>
          <div className="p-3 bg-quantum-dark-300 rounded-lg">
            <p className="text-sm text-quantum-light-300">Quantum</p>
            <p className="text-lg font-bold text-quantum-light-100">
              {formatPercentage(confidence.quantum)}
            </p>
          </div>
        </div>
      </div>
    </Card>
  )
}