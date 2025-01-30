import { Component, ErrorInfo, ReactNode } from 'react'
import { motion } from 'framer-motion'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  }

  public static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
    }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col items-center justify-center min-h-[400px] bg-quantum-dark-200 rounded-lg p-8"
        >
          <div className="text-quantum-accent text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-quantum-accent mb-4">
            Something went wrong
          </h2>
          <p className="text-quantum-light-300 mb-6 text-center max-w-md">
            {this.state.error?.message || 'An unexpected error occurred'}
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-6 py-2 bg-quantum-primary text-quantum-light-100 rounded-lg hover:bg-opacity-90 transition-colors"
            onClick={() => this.setState({ hasError: false, error: null })}
          >
            Try again
          </motion.button>
        </motion.div>
      )
    }

    return this.props.children
  }
}