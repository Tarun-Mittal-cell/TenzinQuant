import { motion } from 'framer-motion'
import { formatPercentage } from '@utils/format'

interface PortfolioAnalysisProps {
  returns: number | null | undefined
  risk: number | null | undefined
  sharpeRatio: number | null | undefined
}

export function PortfolioAnalysis({ returns, risk, sharpeRatio }: PortfolioAnalysisProps) {
  const metrics = [
    {
      label: 'Returns',
      value: returns,
      format: formatPercentage,
      color: returns && returns >= 0 ? 'text-quantum-primary' : 'text-quantum-accent',
    },
    {
      label: 'Risk',
      value: risk,
      format: formatPercentage,
      color: 'text-quantum-accent',
    },
    {
      label: 'Sharpe Ratio',
      value: sharpeRatio,
      format: (value: number) => value.toFixed(2),
      color: sharpeRatio && sharpeRatio >= 1.5 ? 'text-quantum-primary' : 'text-quantum-light-100',
    },
  ]

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold text-quantum-light-100">Portfolio Analysis</h2>
      <div className="grid grid-cols-3 gap-4">
        {metrics.map((metric) => (
          <motion.div
            key={metric.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-quantum-dark-300 rounded-lg p-4"
          >
            <p className="text-quantum-light-300 text-sm">{metric.label}</p>
            <p className={`text-2xl font-bold ${metric.color}`}>
              {metric.value === null || metric.value === undefined
                ? 'N/A'
                : metric.format(metric.value)}
            </p>
          </motion.div>
        ))}
      </div>
      <div className="mt-4 text-quantum-light-300 text-sm">
        <p>
          {sharpeRatio && sharpeRatio >= 1.5
            ? '✨ Your portfolio is performing well with good risk-adjusted returns.'
            : '⚠️ Consider optimizing your portfolio for better risk-adjusted returns.'}
        </p>
      </div>
    </div>
  )
}