import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Route, Switch } from 'wouter'
import { Suspense, lazy, useEffect } from 'react'
import { GlobalErrorBoundary } from '@/components/GlobalErrorBoundary'
import { Navbar } from '@/components/Navbar'
import { Sidebar } from '@/components/Sidebar'
import { LoadingScreen } from '@/components/LoadingScreen'
import { useWebSocketStore } from '@/services/websocket'
import { monitoring, reportPerformanceMetric } from '@/services/monitoring'

// Lazy load pages
const Dashboard = lazy(() => import('@pages/Dashboard'))
const Portfolio = lazy(() => import('@pages/Portfolio'))
const MarketAnalysis = lazy(() => import('@pages/MarketAnalysis'))
const Predictions = lazy(() => import('@pages/Predictions'))
const Settings = lazy(() => import('@pages/Settings'))

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
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
      suspense: true,
      onError: (error) => {
        monitoring.reportError(error as Error)
      },
    },
  },
})

function Router() {
  const { connect, disconnect } = useWebSocketStore()

  useEffect(() => {
    // Connect to WebSocket
    connect()

    // Monitor performance
    const observer = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        reportPerformanceMetric(entry.name, entry.duration)
      })
    })

    observer.observe({ entryTypes: ['navigation', 'resource', 'paint'] })

    return () => {
      disconnect()
      observer.disconnect()
    }
  }, [connect, disconnect])

  return (
    <div className="flex h-screen bg-quantum-dark-400 text-quantum-light-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-quantum-dark-300 p-6">
          <GlobalErrorBoundary>
            <Suspense fallback={<LoadingScreen />}>
              <Switch>
                <Route path="/" component={Dashboard} />
                <Route path="/portfolio" component={Portfolio} />
                <Route path="/market-analysis" component={MarketAnalysis} />
                <Route path="/predictions" component={Predictions} />
                <Route path="/settings" component={Settings} />
              </Switch>
            </Suspense>
          </GlobalErrorBoundary>
        </main>
      </div>
    </div>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router />
    </QueryClientProvider>
  )
}