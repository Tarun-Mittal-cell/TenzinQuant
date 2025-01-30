import asyncio
import websockets
import json
import logging
from typing import Dict, List, Optional, Callable
import yaml
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.config = self._load_config()
        self.connections: Dict[str, websockets.WebSocketClientProtocol] = {}
        self.callbacks: Dict[str, List[Callable]] = {}
        self.running = False
        
    def _load_config(self) -> dict:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    async def connect(self, symbol: str, callback: Optional[Callable] = None):
        """Connect to websocket for a given symbol"""
        if callback:
            if symbol not in self.callbacks:
                self.callbacks[symbol] = []
            self.callbacks[symbol].append(callback)
            
        if symbol not in self.connections:
            # Use free data sources
            ws_url = f"wss://ws.finnhub.io?symbol={symbol}"
            
            retries = 0
            while retries < self.config['websocket']['max_retries']:
                try:
                    self.connections[symbol] = await websockets.connect(ws_url)
                    logger.info(f"Connected to websocket for {symbol}")
                    break
                except Exception as e:
                    logger.error(f"Failed to connect to {symbol}: {e}")
                    retries += 1
                    await asyncio.sleep(self.config['websocket']['reconnect_interval'])
    
    async def disconnect(self, symbol: str):
        """Disconnect from websocket for a given symbol"""
        if symbol in self.connections:
            await self.connections[symbol].close()
            del self.connections[symbol]
            logger.info(f"Disconnected from websocket for {symbol}")
    
    async def start_listening(self):
        """Start listening to all websocket connections"""
        self.running = True
        while self.running:
            for symbol, ws in self.connections.items():
                try:
                    message = await ws.recv()
                    data = json.loads(message)
                    
                    # Process callbacks
                    if symbol in self.callbacks:
                        for callback in self.callbacks[symbol]:
                            await callback(data)
                            
                except websockets.exceptions.ConnectionClosed:
                    logger.warning(f"Connection closed for {symbol}, attempting to reconnect...")
                    await self.connect(symbol)
                except Exception as e:
                    logger.error(f"Error processing message for {symbol}: {e}")
    
    def stop(self):
        """Stop listening to all websocket connections"""
        self.running = False
        
    async def close_all(self):
        """Close all websocket connections"""
        for symbol in list(self.connections.keys()):
            await self.disconnect(symbol)
            
class DataStreamManager:
    def __init__(self):
        self.ws_manager = WebSocketManager()
        self.cache = {}
        
    async def start_streaming(self, symbols: List[str], callback: Callable):
        """Start streaming data for given symbols"""
        for symbol in symbols:
            await self.ws_manager.connect(symbol, callback)
        await self.ws_manager.start_listening()
        
    async def stop_streaming(self):
        """Stop streaming all data"""
        self.ws_manager.stop()
        await self.ws_manager.close_all()
        
    def get_latest_price(self, symbol: str) -> Optional[float]:
        """Get latest cached price for a symbol"""
        return self.cache.get(symbol)
        
    async def price_update_callback(self, data: dict):
        """Callback for price updates"""
        if 'data' in data:
            for trade in data['data']:
                symbol = trade['s']
                price = trade['p']
                self.cache[symbol] = price