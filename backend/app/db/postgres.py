import asyncio
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings
from app.db.base_class import Base

# Engine optimized for high-concurrency SRE tasks
engine = create_async_engine(
    settings.POSTGRES_URL,
    pool_size=20,
    max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Physical table creation with retry logic."""
    retries = 5
    while retries > 0:
        try:
            async with engine.begin() as conn:
                # Local import to avoid circular dependencies
                from app.models.schemas import WorkItem, RcaRecord
                await conn.run_sync(Base.metadata.create_all)
            print("SRE: Database tables initialized successfully.")
            break
        except Exception as e:
            retries -= 1
            print(f"SRE: DB connection waiting... ({retries} retries left)")
            await asyncio.sleep(2)

async def create_work_item(session: AsyncSession, component_id: str, severity: str, message: str):
    """Debouncing Logic: Only create 1 incident if one is already OPEN."""
    from app.models.schemas import WorkItem
    
    query = await session.execute(
        select(WorkItem).where(
            WorkItem.component_id == component_id,
            WorkItem.status == "OPEN"
        )
    )
    existing = query.scalars().first()

    if not existing:
        new_item = WorkItem(
            component_id=component_id,
            severity=severity,
            initial_message=message,
            status="OPEN",
            created_at=datetime.utcnow()
        )
        session.add(new_item)
        await session.commit()
        print(f"SRE: Created NEW incident for {component_id}")
        return new_item
    
    return existing