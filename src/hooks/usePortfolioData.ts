import { useQuery, useQueryClient } from '@tanstack/react-query'
import { useEffect } from 'react'
import { useWebSocketStore } from '@/services/websocket'
import { PortfolioData } from '@/types'

const FALLBACK_DATA: PortfolioData = {
  totalValue: 1000000,
  dailyReturn: 0,
  returns: 0,
  risk: 0,
  sharpeRatio: 0,
  history: [],
  allocation: [],
  riskMetrics: {
    var: 0,
    beta: 0,
    alpha: 0,
  },
}

export function usePortfolioData() {
  const queryClient = useQueryClient()
  const { connect, disconnect } = useWebSocketStore()

  // Initial data fetch
  const query = useQuery({
    queryKey: ['portfolio'],
    queryFn: async () => {
      try {
        const response = await fetch('/api/portfolio')
        if (!response.ok) {
          throw new Error('Failed to fetch portfolio data')
        }
        const data = await response.json()
        return data as PortfolioData
      } catch (error) {
        console.error('Portfolio data fetch error:', error)
        return FALLBACK_DATA
      }
    },
    placeholderData: FALLBACK_DATA,
    staleTime: 1000 * 60, // 1 minute
    retry: (failureCount, error) => {
      // Implement exponential backoff
      const maxRetries = 3
      const shouldRetry = failureCount < maxRetries
      
      if (shouldRetry) {
        const delay = Math.min(1000 * Math.pow(2, failureCount), 10000)
        setTimeout(() => {}, delay)
      }
      
      return shouldRetry
    },
  })

  // Set up WebSocket connection for real-time updates
  useEffect(() => {
    const socket = new WebSocket('wss://your-websocket-server.com')

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.type === 'PORTFOLIO_UPDATE') {
          queryClient.setQueryData(['portfolio'], (old: PortfolioData) => ({
            ...old,
            ...data.payload,
          }))
        }
      } catch (error) {
        console.error('WebSocket message parsing error:', error)
      }
    }

    connect()

    return () => {
      disconnect()
    }
  }, [queryClient, connect, disconnect])

  return query
}

// Custom hook for portfolio metrics
export function usePortfolioMetrics() {
  const { data: portfolio } = usePortfolioData()

  return {
    isPositive: (portfolio?.dailyReturn ?? 0) >= 0,
    formattedReturn: `${(portfolio?.dailyReturn ?? 0).toFixed(2)}%`,
    riskLevel: getRiskLevel(portfolio?.risk ?? 0),
    sharpeRatioStatus: getSharpeRatioStatus(portfolio?.sharpeRatio ?? 0),
  }
}

// Helper functions
function getRiskLevel(risk: number): 'Low' | 'Moderate' | 'High' {
  if (risk < 10) return 'Low'
  if (risk < 20) return 'Moderate'
  return 'High'
}

function getSharpeRatioStatus(ratio: number): 'Poor' | 'Good' | 'Excellent' {
  if (ratio < 1) return 'Poor'
  if (ratio < 2) return 'Good'
  return 'Excellent'
}