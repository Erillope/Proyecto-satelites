from pydantic import BaseModel
from datetime import time
import pandas as pd

class DatosSatelite(BaseModel):
    segundo: int
    prx: float
    is_visible_outer: bool = False


class Satelite(BaseModel):
    id: str
    datos: list[DatosSatelite] = []


class XLSXLectorSatelite:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.satelites : dict[str, Satelite] = {}
    
    def read_data(self) -> list[Satelite]:
        print(f"Leyendo datos del archivo: {self.file_path}")
        df = pd.read_excel(
            self.file_path,
            usecols=["Hora", "Sat_ID", "PRx", "is_visible_outer"],
        )

        for i, row in df.iterrows():
            print(f"Procesando fila numero {i}")

            if row["Sat_ID"] not in self.satelites:
                self.satelites[row["Sat_ID"]] = Satelite(id=row["Sat_ID"])

            self.satelites[row["Sat_ID"]].datos.append(self._map_datos(row))
        
        return list(self.satelites.values())
    
    def _calcular_segundos(self, hora: str) -> int:
        hora_time = time.fromisoformat(hora)
        return hora_time.hour * 3600 + hora_time.minute * 60 + hora_time.second
    
    def _map_datos(self, row: pd.Series) -> DatosSatelite:
        return DatosSatelite(
            segundo=self._calcular_segundos(row["Hora"]),
            prx=round(row["PRx"], 2),
            is_visible_outer=row["is_visible_outer"]
        )
