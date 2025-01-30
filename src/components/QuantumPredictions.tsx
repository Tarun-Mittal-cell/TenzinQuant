import { motion, AnimatePresence } from 'framer-motion'
import { useQuantumPredictions } from '@/services/quantum-predictor'
import { formatCurrency, formatPercentage } from '@/utils/format'
import { Card } from '@tremor/react'
import { Brain, TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react'

interface QuantumPredictionsProps {
  symbols: string[]
}

export function QuantumPredictions({ symbols }: QuantumPredictionsProps) {
  const { predictions, marketRegime, confidence, lastUpdate, isProcessing } = useQuantumPredictions(symbols)

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-quantum-light-100">
          Quantum Predictions
        </h2>
        <div className="flex items-center space-x-2 text-quantum-light-300">
          <Brain className="w-5 h-5" />
          <span>Market Regime: {marketRegime.replace('_', ' ')}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <AnimatePresence mode="popLayout">
          {predictions?.map((prediction) => (
            prediction && (
              <motion.div
                key={prediction.symbol}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                layout
              >
                <Card className="bg-quantum-dark-200 p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="text-xl font-bold text-quantum-light-100">
                        {prediction.symbol}
                      </h3>
                      <p className={`text-sm ${
                        prediction.signal === 'BUY' ? 'text-quantum-primary' :
                        prediction.signal === 'SELL' ? 'text-quantum-accent' :
                        'text-quantum-light-300'
                      }`}>
                        {prediction.signal} • {formatPercentage(prediction.confidence.overall)}
                      </p>
                    </div>
                    {prediction.signal === 'BUY' ? (
                      <TrendingUp className="w-6 h-6 text-quantum-primary" />
                    ) : prediction.signal === 'SELL' ? (
                      <TrendingDown className="w-6 h-6 text-quantum-accent" />
                    ) : (
                      <AlertTriangle className="w-6 h-6 text-quantum-light-300" />
                    )}
                  </div>

                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-quantum-light-300">Expected Price</p>
                        <p className="text-lg font-bold text-quantum-light-100">
                          {formatCurrency(prediction.priceTargets.expected)}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-quantum-light-300">Confidence</p>
                        <div className="flex items-center space-x-2">
                          <div className="flex-1 h-2 bg-quantum-dark-300 rounded-full">
                            <motion.div
                              className="h-full bg-quantum-primary rounded-full"
                              initial={{ width: 0 }}
                              animate={{ width: `${prediction.confidence.quantum * 100}%` }}
                              transition={{ duration: 0.5 }}
                            />
                          </div>
                          <span className="text-sm text-quantum-light-100">
                            {formatPercentage(prediction.confidence.quantum)}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <h4 className="text-sm font-medium text-quantum-light-300">Analysis</h4>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div className={`p-2 rounded ${
                          prediction.analysis.technical.signal === 'BULLISH'
                            ? 'bg-quantum-primary bg-opacity-20'
                            : 'bg-quantum-accent bg-opacity-20'
                        }`}>
                          <p className="text-quantum-light-300">Technical</p>
                          <p className="font-medium">
                            {prediction.analysis.technical.signal}
                          </p>
                        </div>
                        <div className={`p-2 rounded ${
                          prediction.analysis.fundamental.signal === 'BULLISH'
                            ? 'bg-quantum-primary bg-opacity-20'
                            : 'bg-quantum-accent bg-opacity-20'
                        }`}>
                          <p className="text-quantum-light-300">Fundamental</p>
                          <p className="font-medium">
                            {prediction.analysis.fundamental.signal}
                          </p>
                        </div>
                        <div className={`p-2 rounded ${
                          prediction.analysis.sentiment.signal === 'BULLISH'
                            ? 'bg-quantum-primary bg-opacity-20'
                            : 'bg-quantum-accent bg-opacity-20'
                        }`}>
                          <p className="text-quantum-light-300">Sentiment</p>
                          <p className="font-medium">
                            {prediction.analysis.sentiment.signal}
                          </p>
                        </div>
                        <div className={`p-2 rounded ${
                          prediction.analysis.quantum.signal === 'BULLISH'
                            ? 'bg-quantum-primary bg-opacity-20'
                            : 'bg-quantum-accent bg-opacity-20'
                        }`}>
                          <p className="text-quantum-light-300">Quantum</p>
                          <p className="font-medium">
                            {prediction.analysis.quantum.signal}
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="pt-4 border-t border-quantum-dark-300">
                      <div className="flex justify-between text-sm">
                        <span className="text-quantum-light-300">
                          Updated {new Date(prediction.timestamp).toLocaleTimeString()}
                        </span>
                        <span className="text-quantum-light-300">
                          Coherence: {formatPercentage(prediction.analysis.quantum.coherence)}
                        </span>
                      </div>
                    </div>
                  </div>
                </Card>
              </motion.div>
            )
          ))}
        </AnimatePresence>
      </div>

      {isProcessing && (
        <div className="flex justify-center">
          <motion.div
            className="w-12 h-12 border-4 border-quantum-primary border-t-transparent rounded-full"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          />
        </div>
      )}

      <div className="flex justify-between items-center text-sm text-quantum-light-300">
        <span>Last update: {lastUpdate.toLocaleTimeString()}</span>
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-quantum-primary" />
            <span>Technical ({formatPercentage(confidence.technical)})</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-quantum-accent" />
            <span>Quantum ({formatPercentage(confidence.quantum)})</span>
          </div>
        </div>
      </div>
    </div>
  )
}