import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.db.postgres import AsyncSessionLocal, create_work_item

# Internal buffer
signal_queue = asyncio.Queue(maxsize=settings.SIGNAL_QUEUE_SIZE)

async def process_batch(batch):
    """Processes signals: All to Mongo (Archive), One to Postgres (Incident)."""
    if not batch:
        return

    # 1. Archive every single raw signal to MongoDB
    try:
        mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
        db = mongo_client.ims_database
        # CRITICAL: Convert Pydantic objects to dictionaries for Mongo
        docs = [s.dict() for s in batch]
        await db.raw_signals.insert_many(docs)
        print(f"SRE WORKER: Archived {len(batch)} signals to MongoDB.")
    except Exception as e:
        print(f"SRE MONGO ERROR: {e}")

    # 2. Update Postgres (Debouncing)
    try:
        representative = batch[0]
        async with AsyncSessionLocal() as session:
            await create_work_item(
                session,
                component_id=representative.component_id,
                severity=representative.severity,
                message=representative.error_message
            )
    except Exception as e:
        print(f"SRE POSTGRES ERROR: {e}")

async def signal_processor():
    """The infinite loop that drains the queue."""
    print("SRE WORKER: Background consumer active and waiting for signals...")
    while True:
        try:
            # Wait for at least one signal
            signal = await signal_queue.get()
            batch = [signal]

            # Collect up to 100 more signals if they are ready (Batching)
            while not signal_queue.empty() and len(batch) < 100:
                batch.append(signal_queue.get_nowait())

            await process_batch(batch)

            for _ in range(len(batch)):
                signal_queue.task_done()
        except Exception as fatal_e:
            print(f"SRE WORKER CRITICAL FAILURE: {fatal_e}")
            await asyncio.sleep(1)