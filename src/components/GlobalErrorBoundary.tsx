import { Component, ErrorInfo, ReactNode } from 'react'
import { motion } from 'framer-motion'
import { AlertTriangle } from 'lucide-react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
  errorInfo: ErrorInfo | null
}

export class GlobalErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null,
  }

  public static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo)
    
    // Send error to monitoring service
    this.logError(error, errorInfo)
  }

  private logError = async (error: Error, errorInfo: ErrorInfo) => {
    try {
      await fetch('/api/log-error', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          error: {
            message: error.message,
            stack: error.stack,
          },
          errorInfo,
          timestamp: new Date().toISOString(),
          url: window.location.href,
          userAgent: navigator.userAgent,
        }),
      })
    } catch (e) {
      console.error('Failed to log error:', e)
    }
  }

  private handleReload = () => {
    window.location.reload()
  }

  private handleReportIssue = () => {
    const body = `Error: ${this.state.error?.message}\n\nStack: ${this.state.error?.stack}`
    window.open(`mailto:support@tenzinquantum.com?subject=Bug Report&body=${encodeURIComponent(body)}`)
  }

  public render() {
    if (this.state.hasError) {
      return (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="min-h-screen bg-quantum-dark-400 flex items-center justify-center p-4"
        >
          <div className="max-w-md w-full bg-quantum-dark-300 rounded-lg p-8 text-center">
            <motion.div
              animate={{ 
                scale: [1, 1.2, 1],
                rotate: [0, 10, -10, 0] 
              }}
              transition={{ duration: 0.5 }}
              className="inline-block mb-6 text-quantum-accent"
            >
              <AlertTriangle size={48} />
            </motion.div>
            
            <h1 className="text-2xl font-bold text-quantum-light-100 mb-4">
              Something went wrong
            </h1>
            
            <p className="text-quantum-light-300 mb-6">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            
            <div className="space-y-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="w-full px-6 py-2 bg-quantum-primary text-quantum-light-100 rounded-lg hover:bg-opacity-90 transition-colors"
                onClick={this.handleReload}
              >
                Try Again
              </motion.button>
              
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="w-full px-6 py-2 border border-quantum-light-300 text-quantum-light-100 rounded-lg hover:bg-quantum-dark-200 transition-colors"
                onClick={this.handleReportIssue}
              >
                Report Issue
              </motion.button>
            </div>

            {process.env.NODE_ENV === 'development' && (
              <div className="mt-8 text-left">
                <details className="text-quantum-light-300 text-sm">
                  <summary className="cursor-pointer mb-2">Error Details</summary>
                  <pre className="bg-quantum-dark-400 p-4 rounded-lg overflow-auto">
                    {this.state.error?.stack}
                  </pre>
                </details>
              </div>
            )}
          </div>
        </motion.div>
      )
    }

    return this.props.children
  }
}