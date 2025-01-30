from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
import uvicorn
import asyncio
import logging
from datetime import datetime
import yaml
from services.market_data import MarketDataService
from models.quantum_predictor import QuantumPredictor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize FastAPI app
app = FastAPI(
    title="Quantum Trading API",
    description="High-performance trading API with real-time market data and AI predictions",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
market_data = MarketDataService()
predictor = QuantumPredictor()

# WebSocket connections store
connections: Dict[str, List[WebSocket]] = {}

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Quantum Trading API server...")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Quantum Trading API server...")
    await market_data.stop_streaming()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time market data"""
    await websocket.accept()
    
    if client_id not in connections:
        connections[client_id] = []
    connections[client_id].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if 'subscribe' in data:
                # Start streaming for new symbols
                symbols = data['subscribe']
                await market_data.start_streaming(symbols)
                
            elif 'unsubscribe' in data:
                # Stop streaming for symbols
                symbols = data['unsubscribe']
                for symbol in symbols:
                    await market_data.stop_streaming()
                    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        connections[client_id].remove(websocket)
        if not connections[client_id]:
            del connections[client_id]

async def broadcast_market_data(symbol: str, price: float):
    """Broadcast market data to all connected clients"""
    message = {
        'symbol': symbol,
        'price': price,
        'timestamp': datetime.now().isoformat()
    }
    
    for client_connections in connections.values():
        for connection in client_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")

@app.get("/api/v1/market/summary")
async def get_market_summary(symbols: List[str]):
    """Get market summary for multiple symbols"""
    try:
        return market_data.get_market_summary(symbols)
    except Exception as e:
        logger.error(f"Error getting market summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/market/historical/{symbol}")
async def get_historical_data(symbol: str, period: str = "1y"):
    """Get historical market data"""
    try:
        data = market_data.get_historical_data(symbol, period)
        return data.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Error getting historical data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/predictions")
async def get_predictions(symbols: List[str]):
    """Get AI predictions for multiple symbols"""
    try:
        return predictor.get_predictions(symbols)
    except Exception as e:
        logger.error(f"Error getting predictions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/market/price/{symbol}")
async def get_real_time_price(symbol: str):
    """Get real-time price for a symbol"""
    try:
        price = market_data.get_real_time_price(symbol)
        if price is None:
            raise HTTPException(status_code=404, detail=f"Price not found for {symbol}")
        return {"symbol": symbol, "price": price}
    except Exception as e:
        logger.error(f"Error getting price: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )