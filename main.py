from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
from datetime import datetime

app = FastAPI()

# Keep the hello world endpoint
@app.get("/")
def read_root():
    return {"greeting": "Hello, World!", "message": "Forex Webhook Active!"}

# Forex trading signal model
class TradingSignal(BaseModel):
    pair: str
    direction: str
    risk_percent: float
    entry: float
    sl: float
    tp1: float
    tp2: Optional[float] = None
    prob_score: float
    iof_score: float

# Main webhook endpoint for your Python core
@app.post("/webhook")
async def webhook(signal: TradingSignal):
    """Receive trading signals from Python core engine"""
    timestamp = datetime.utcnow().isoformat()
    print(f"[{timestamp}] Signal: {signal.pair} {signal.direction} @ {signal.entry}")
    
    return {
        "status": "success",
        "message": f"Signal processed for {signal.pair}",
        "timestamp": timestamp,
        "data": signal.dict()
    }

# Alternative webhook for TradingView
@app.post("/webhook/tradingview")
async def tradingview_webhook(request: Request):
    """Receive webhooks from TradingView"""
    try:
        body = await request.body()
        data = json.loads(body) if body else {}
        print(f"TradingView webhook received: {data}")
        return {"status": "received", "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "Forex Hybrid Webhook",
        "endpoints": ["/", "/webhook", "/webhook/tradingview", "/health"]
    }

# Recent signals endpoint (for monitoring)
@app.get("/status")
def get_status():
    return {
        "service": "Forex Trading Webhook",
        "version": "1.0",
        "ready": True,
        "webhook_url": "https://fastapi-production-abac.up.railway.app/webhook"
    }
