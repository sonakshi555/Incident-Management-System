import asyncio
from fastapi import FastAPI, HTTPException
from app.workers.ingestor import signal_queue, signal_processor
from app.models.schemas import Signal
from app.db.postgres import init_db
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from app.db.postgres import AsyncSessionLocal
from app.models.schemas import WorkItem

app = FastAPI(title="Mission-Critical IMS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your Live Server (port 5500) to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    print("SRE API: Starting lifecycle management...")
    # 1. Physical DB Setup
    await init_db()
    # 2. Start Background Consumer
    asyncio.create_task(signal_processor())
    print("SRE API: Startup complete.")

@app.get("/incidents")
async def get_incidents():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(WorkItem).order_by(WorkItem.created_at.desc()))
        return result.scalars().all()

@app.post("/ingest")
async def ingest_signal(signal: Signal):
    if signal_queue.full():
        raise HTTPException(status_code=503, detail="Backpressure: Buffer Full")
    await signal_queue.put(signal)
    return {"status": "queued"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}