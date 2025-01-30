import { motion } from 'framer-motion'
import { useQuery } from '@tanstack/react-query'
import { Card } from '@tremor/react'
import { PortfolioAnalysis } from '@components/PortfolioAnalysis'
import { PortfolioChart } from '@components/PortfolioChart'
import { RiskMetrics } from '@components/RiskMetrics'
import { AssetAllocation } from '@components/AssetAllocation'
import { getPortfolioData } from '@services/portfolio'
import { formatCurrency, formatPercentage } from '@utils/format'

export default function Portfolio() {
  const { data: portfolio } = useQuery({
    queryKey: ['portfolio'],
    queryFn: getPortfolioData,
  })

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Portfolio Overview</h1>
        <div className="flex space-x-4">
          <div className="text-right">
            <p className="text-quantum-light-300">Total Value</p>
            <p className="text-2xl font-bold text-quantum-light-100">
              {formatCurrency(portfolio?.totalValue ?? 0)}
            </p>
          </div>
          <div className="text-right">
            <p className="text-quantum-light-300">Today's Return</p>
            <p className={`text-2xl font-bold ${
              (portfolio?.dailyReturn ?? 0) >= 0 
                ? 'text-quantum-primary' 
                : 'text-quantum-accent'
            }`}>
              {formatPercentage(portfolio?.dailyReturn ?? 0)}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="bg-quantum-dark-200 p-6">
          <PortfolioChart data={portfolio?.history ?? []} />
        </Card>
        <Card className="bg-quantum-dark-200 p-6">
          <PortfolioAnalysis 
            returns={portfolio?.returns} 
            risk={portfolio?.risk}
            sharpeRatio={portfolio?.sharpeRatio}
          />
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="bg-quantum-dark-200 p-6">
          <AssetAllocation allocation={portfolio?.allocation ?? []} />
        </Card>
        <Card className="bg-quantum-dark-200 p-6">
          <RiskMetrics metrics={portfolio?.riskMetrics} />
        </Card>
      </div>
    </motion.div>
  )
}