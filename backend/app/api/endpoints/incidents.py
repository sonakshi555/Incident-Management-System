from fastapi import APIRouter, HTTPException
from app.services.workflow import IncidentWorkflow
from app.models.schemas import RCA, WorkItemUpdate

router = APIRouter()

@router.get("/")
async def list_incidents():
    # Logic to fetch active incidents from Redis/Postgres
    return {"incidents": []}

@router.patch("/{incident_id}/status")
async def update_incident_status(incident_id: str, update: WorkItemUpdate):
    """
    Handles state transitions using the State Pattern.
    Rejects transition to CLOSED if RCA is missing.
    """
    workflow = IncidentWorkflow(incident_id)
    try:
        new_status = await workflow.transition_to(update.status, update.rca_data)
        return {"incident_id": incident_id, "new_status": new_status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))