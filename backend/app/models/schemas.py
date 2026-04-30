from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# Use 'String' instead of 'str' for SQLAlchemy columns
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# --- SQLAlchemy Models (Database Tables) ---

class WorkItem(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(String, index=True)
    severity = Column(String)
    initial_message = Column(String)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    rca = relationship("RcaRecord", back_populates="incident", uselist=False)

class RcaRecord(Base):
    __tablename__ = "rca_records"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), unique=True)
    category = Column(String)
    fix_applied = Column(String)
    prevention_steps = Column(String)
    resolved_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("WorkItem", back_populates="rca")

# --- Pydantic Models (API Validation) ---

class Signal(BaseModel):
    component_id: str
    error_message: str
    severity: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class RCACreate(BaseModel):
    category: str
    fix_applied: str
    prevention_steps: str

class IncidentOut(BaseModel):
    id: int
    component_id: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True