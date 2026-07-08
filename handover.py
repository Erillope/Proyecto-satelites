from repository import Satelite
from pydantic import BaseModel
from datetime import time
from enum import Enum

class CriticalPointType(str, Enum):
    SWITCH = "switch"
    NOT_FOUND = "not_found"
    RECONNECT = "reconnect"

class CriticalPoint(BaseModel):
    time: time
    sat_id: str | None
    type: CriticalPointType

class Handover:
    def __init__(self, threshold: float) -> None:
        self.critical_points: list[CriticalPoint] = []
        self.threshold = threshold

    def execute(self, current_sat: Satelite | None, satelites: list[Satelite], time: time) -> Satelite | None:
        if len(satelites) == 0:
            if current_sat is not None:
                self.critical_points.append(CriticalPoint(time=time, sat_id=None, type=CriticalPointType.NOT_FOUND))
            return None
        
        if current_sat is None:
            sat_max = max(satelites, key=lambda s: s.prx)
            self.critical_points.append(CriticalPoint(time=time, sat_id=sat_max.id, type=CriticalPointType.RECONNECT))
            return sat_max
        
        current_sat = next((s for s in satelites if s.id == current_sat.id))

        if current_sat.prx >= self.threshold:
            return current_sat
        
        else:
            sat_max = max(satelites, key=lambda s: s.prx)
            if sat_max.prx > current_sat.prx:
                self.critical_points.append(CriticalPoint(time=time, sat_id=sat_max.id, type=CriticalPointType.SWITCH))
                return sat_max
            return current_sat
    
    def generate_log(self, log_file: str) -> None:
        with open(log_file, "w", encoding="utf-8") as f:
            for cp in self.critical_points:
                if cp.type == CriticalPointType.SWITCH:
                    f.write(f"[{cp.type.upper()}]: Se realizó un cambio de satélite a las {cp.time} hacia el satélite {cp.sat_id}.\n")
                elif cp.type == CriticalPointType.NOT_FOUND:
                    f.write(f"[{cp.type.upper()}]: Pérdida de conexión a las {cp.time}.\n")
                elif cp.type == CriticalPointType.RECONNECT:
                    f.write(f"[{cp.type.upper()}]: Se reconectó al satélite {cp.sat_id} a las {cp.time}.\n")