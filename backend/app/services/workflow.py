from abc import ABC, abstractmethod

class IncidentState(ABC):
    @abstractmethod
    def transition(self, target_status: str, has_rca: bool):
        pass

class OpenState(IncidentState):
    def transition(self, target_status, has_rca):
        if target_status == "INVESTIGATING": return "INVESTIGATING"
        return "OPEN"

class InvestigatingState(IncidentState):
    def transition(self, target_status, has_rca):
        if target_status == "RESOLVED": return "RESOLVED"
        return "INVESTIGATING"

class ResolvedState(IncidentState):
    def transition(self, target_status, has_rca):
        if target_status == "CLOSED":
            if not has_rca:
                raise ValueError("Mandatory RCA missing for CLOSING")
            return "CLOSED"
        return "RESOLVED"