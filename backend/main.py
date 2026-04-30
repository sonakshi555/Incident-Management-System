import asyncio
from fastapi import FastAPI, HTTPException
from app.workers.ingestor import signal_queue, signal_processor
from app.models.schemas import Signal
from app.db.postgres import init_db

app = FastAPI(title="Mission-Critical IMS")

@app.on_event("startup")
async def startup_event():
    print("SRE API: Starting lifecycle management...")
    # 1. Physical DB Setup
    await init_db()
    # 2. Start Background Consumer
    asyncio.create_task(signal_processor())
    print("SRE API: Startup complete.")

@app.post("/ingest")
async def ingest_signal(signal: Signal):
    if signal_queue.full():
        raise HTTPException(status_code=503, detail="Backpressure: Buffer Full")
    await signal_queue.put(signal)
    return {"status": "queued"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}