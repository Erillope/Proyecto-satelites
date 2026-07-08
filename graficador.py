from repository import Satelite
from typing import Dict, List, Tuple
from datetime import datetime
from handover import CriticalPoint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import time

Color = str
CurvaPotencias = Tuple[Color, Tuple[List[time], List[float]]]

class GraficadorCurvasPotencias:
    def __init__(self) -> None:
        self.curvas: Dict[str, CurvaPotencias] = {}
    
    def add_all_curvas(self, satelites: List[Satelite], t: time) -> None:
        for satelite in satelites:
            self.add_curva(satelite, t)

    def add_curva(self, satelite: Satelite, t: time) -> None:
        if satelite.id not in self.curvas:
            self.curvas[satelite.id] = (satelite.color, ([], []))
        self.curvas[satelite.id][1][0].append(t)
        self.curvas[satelite.id][1][1].append(satelite.prx)

    def plot(self, name: str) -> None:
        plt.figure(figsize=(12, 6))
        for (color, (times, prx_values)) in self.curvas.values():
            plt.plot([datetime.combine(datetime.today(), t) for t in times], prx_values, color=color)

        plt.xlabel("Hora")
        plt.ylabel("PRx")
        plt.title(name)
        plt.legend()
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.gca().xaxis.set_major_formatter(
            mdates.DateFormatter("%H:%M:%S")
        )
        plt.savefig(name+'.png')
        plt.show()


class GraficadorHandover:
    def plot(self, critical_points: List[CriticalPoint], time_range: List[time], muestras_prx: List[float], name: str) -> None:
        plt.figure(figsize=(12, 6))
        plt.plot([datetime.combine(datetime.today(), t) for t in time_range], muestras_prx)

        for critical_point in critical_points:
            if critical_point.type == "switch":
                color = "orange"
            elif critical_point.type == "not_found":
                color = "red"
            elif critical_point.type == "reconnect":
                color = "green"
            plt.axvline(datetime.combine(datetime.today(), critical_point.time), color=color, linestyle='--', alpha=0.5)

        plt.xlabel("Hora")
        plt.ylabel("PRx")
        plt.title(name)
        plt.grid()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        plt.savefig(name+'.png')
        plt.show()