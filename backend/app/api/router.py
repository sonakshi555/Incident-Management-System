from fastapi import APIRouter
from app.api.endpoints import ingestion, incidents

api_router = APIRouter()
api_router.include_router(ingestion.router, prefix="/ingest", tags=["Ingestion"])
api_router.include_router(incidents.router, prefix="/incidents", tags=["Incidents"])