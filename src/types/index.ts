export type MarketRegime = 
  | 'BULLISH_TREND'
  | 'BEARISH_TREND'
  | 'HIGH_VOLATILITY'
  | 'LOW_VOLATILITY'
  | 'MEAN_REVERTING'
  | 'MOMENTUM'
  | 'NEUTRAL'

export type TradingSignal = 'BUY' | 'SELL' | 'HOLD'
export type SignalStrength = 'BULLISH' | 'BEARISH'

export interface ModelConfidence {
  overall: number
  technical: number
  fundamental: number
  sentiment: number
  quantum: number
}

export interface PriceTargets {
  bullish: number
  bearish: number
  expected: number
}

export interface TechnicalAnalysis {
  signal: SignalStrength
  strength: number
  indicators: {
    rsi: number
    macd: number
    bollingerBands: {
      upper: number
      middle: number
      lower: number
    }
  }
}

export interface FundamentalAnalysis {
  signal: SignalStrength
  strength: number
  metrics: {
    peRatio: number
    pbRatio: number
    debtToEquity: number
  }
}

export interface SentimentAnalysis {
  signal: SignalStrength
  strength: number
  sources: {
    news: number
    social: number
    insider: number
  }
}

export interface QuantumAnalysis {
  signal: SignalStrength
  strength: number
  entropy: number
  coherence: number
}

export interface PredictionResult {
  symbol: string
  signal: TradingSignal
  confidence: ModelConfidence
  priceTargets: PriceTargets
  timestamp: Date
  analysis: {
    technical: TechnicalAnalysis
    fundamental: FundamentalAnalysis
    sentiment: SentimentAnalysis
    quantum: QuantumAnalysis
  }
}

export interface StockData {
  symbol: string
  price: number
  change: number
  volume: number
  marketCap: number
  peRatio: number
  dividend: number
  historicalPrices: {
    date: Date
    price: number
    volume: number
  }[]
}

export interface PortfolioPosition {
  symbol: string
  shares: number
  averageCost: number
  currentValue: number
  unrealizedGain: number
  weight: number
  riskScore: number
  performance: {
    daily: number
    weekly: number
    monthly: number
    yearly: number
  }
}

export interface RiskMetrics {
  var: number // Value at Risk
  beta: number
  alpha: number
  sharpeRatio: number
  sortinoRatio: number
  maxDrawdown: number
  correlations: Record<string, number>
}

export interface PortfolioAnalytics {
  totalValue: number
  cashBalance: number
  positions: PortfolioPosition[]
  performance: {
    daily: number
    weekly: number
    monthly: number
    yearly: number
  }
  riskMetrics: RiskMetrics
  diversification: {
    sectorWeights: Record<string, number>
    geographicWeights: Record<string, number>
    assetClassWeights: Record<string, number>
  }
  recommendations: {
    type: 'BUY' | 'SELL' | 'REBALANCE'
    symbol?: string
    reason: string
    impact: number
    confidence: number
  }[]
}

export interface MarketData {
  indices: {
    name: string
    value: number
    change: number
  }[]
  sectors: {
    name: string
    performance: number
    momentum: number
  }[]
  currencies: {
    pair: string
    rate: number
    change: number
  }[]
  commodities: {
    name: string
    price: number
    change: number
  }[]
  globalMarkets: {
    region: string
    performance: number
    status: 'OPEN' | 'CLOSED'
  }[]
}

export interface NewsItem {
  id: string
  title: string
  summary: string
  source: string
  url: string
  sentiment: number
  relevance: number
  timestamp: Date
  tickers: string[]
  categories: string[]
}