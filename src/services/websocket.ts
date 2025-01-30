import { create } from 'zustand'

interface WebSocketStore {
  socket: WebSocket | null
  connected: boolean
  connect: () => void
  disconnect: () => void
  sendMessage: (message: any) => void
}

export const useWebSocketStore = create<WebSocketStore>((set, get) => ({
  socket: null,
  connected: false,

  connect: () => {
    if (get().socket) return

    const socket = new WebSocket('wss://your-websocket-server.com')

    socket.onopen = () => {
      console.log('WebSocket connected')
      set({ connected: true })
    }

    socket.onclose = () => {
      console.log('WebSocket disconnected')
      set({ connected: false, socket: null })
      // Attempt to reconnect after 5 seconds
      setTimeout(() => get().connect(), 5000)
    }

    socket.onerror = (error) => {
      console.error('WebSocket error:', error)
      socket.close()
    }

    set({ socket })
  },

  disconnect: () => {
    const { socket } = get()
    if (socket) {
      socket.close()
      set({ socket: null, connected: false })
    }
  },

  sendMessage: (message: any) => {
    const { socket } = get()
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message))
    }
  },
}))