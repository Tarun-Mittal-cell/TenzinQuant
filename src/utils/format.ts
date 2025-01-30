const currencyFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})

const percentFormatter = new Intl.NumberFormat('en-US', {
  style: 'percent',
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})

export function formatCurrency(value: number): string {
  return currencyFormatter.format(value)
}

export function formatPercentage(value: number): string {
  return percentFormatter.format(value / 100)
}

export function formatNumber(value: number | null | undefined): string {
  if (value === null || value === undefined) return 'N/A'
  return value.toFixed(2)
}

export function formatLargeNumber(value: number): string {
  if (value >= 1e9) {
    return `${(value / 1e9).toFixed(2)}B`
  }
  if (value >= 1e6) {
    return `${(value / 1e6).toFixed(2)}M`
  }
  if (value >= 1e3) {
    return `${(value / 1e3).toFixed(2)}K`
  }
  return value.toFixed(2)
}