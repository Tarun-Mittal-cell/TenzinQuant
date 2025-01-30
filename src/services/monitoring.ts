interface ErrorReport {
  message: string
  stack?: string
  componentStack?: string
  timestamp: string
  url: string
  userAgent: string
  tags?: Record<string, string>
}

class MonitoringService {
  private static instance: MonitoringService
  private errorQueue: ErrorReport[] = []
  private isProcessing = false
  private readonly BATCH_SIZE = 10
  private readonly FLUSH_INTERVAL = 5000 // 5 seconds

  private constructor() {
    this.startPeriodicFlush()
  }

  public static getInstance(): MonitoringService {
    if (!MonitoringService.instance) {
      MonitoringService.instance = new MonitoringService()
    }
    return MonitoringService.instance
  }

  public async reportError(error: Error, componentStack?: string, tags?: Record<string, string>) {
    const errorReport: ErrorReport = {
      message: error.message,
      stack: error.stack,
      componentStack,
      timestamp: new Date().toISOString(),
      url: window.location.href,
      userAgent: navigator.userAgent,
      tags,
    }

    this.errorQueue.push(errorReport)

    if (this.errorQueue.length >= this.BATCH_SIZE) {
      await this.flushErrors()
    }
  }

  private async flushErrors() {
    if (this.isProcessing || this.errorQueue.length === 0) return

    this.isProcessing = true

    try {
      const errors = this.errorQueue.splice(0, this.BATCH_SIZE)
      
      await fetch('/api/log-errors', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ errors }),
      })
    } catch (error) {
      console.error('Failed to send error reports:', error)
      // Put the errors back in the queue
      this.errorQueue.unshift(...this.errorQueue.splice(0, this.BATCH_SIZE))
    } finally {
      this.isProcessing = false
    }
  }

  private startPeriodicFlush() {
    setInterval(() => {
      if (this.errorQueue.length > 0) {
        this.flushErrors()
      }
    }, this.FLUSH_INTERVAL)
  }

  public async reportMetric(name: string, value: number, tags?: Record<string, string>) {
    try {
      await fetch('/api/metrics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          value,
          tags,
          timestamp: new Date().toISOString(),
        }),
      })
    } catch (error) {
      console.error('Failed to report metric:', error)
    }
  }

  public async reportEvent(name: string, properties?: Record<string, any>) {
    try {
      await fetch('/api/events', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          properties,
          timestamp: new Date().toISOString(),
          url: window.location.href,
        }),
      })
    } catch (error) {
      console.error('Failed to report event:', error)
    }
  }
}

export const monitoring = MonitoringService.getInstance()

// Error boundary helper
export function logError(error: Error, componentStack: string) {
  monitoring.reportError(error, componentStack, {
    environment: process.env.NODE_ENV,
    version: process.env.NEXT_PUBLIC_VERSION,
  })
}

// Performance monitoring
export function reportPerformanceMetric(name: string, value: number) {
  monitoring.reportMetric(name, value, {
    environment: process.env.NODE_ENV,
  })
}

// User interaction events
export function trackEvent(name: string, properties?: Record<string, any>) {
  monitoring.reportEvent(name, properties)
}