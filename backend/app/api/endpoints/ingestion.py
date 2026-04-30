from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import Signal
from app.core.security import check_rate_limit, validate_api_key
from app.workers.ingestor import signal_queue

router = APIRouter()

@router.post("/", dependencies=[Depends(check_rate_limit), Depends(validate_api_key)])
async def post_signal(signal: Signal):
    """
    High-throughput endpoint. 
    Does not wait for DB; pushes to internal async queue.
    """
    try:
        # Pushing to the queue is O(1)
        signal_queue.put_nowait(signal)
        return {"status": "accepted", "id": signal.component_id}
    except Exception: # If queue is full
        raise HTTPException(status_code=503, detail="System Overloaded: Buffer Full")