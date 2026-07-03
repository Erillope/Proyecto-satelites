from pydantic import BaseModel
from datetime import time
import pandas as pd

class DatosSatelite(BaseModel):
    segundo: int
    prx: float
    is_visible_outer: bool = False
    is_visible_inner: bool = False


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
            usecols=["hora", "sat_id", "PRx", "is_visible_outer", "is_visible_inner"],
        )

        for i, row in df.iterrows():
            print(f"Procesando fila numero {i}")

            if row["sat_id"] not in self.satelites:
                print(row["sat_id"], type(row["sat_id"]))
                self.satelites[row["sat_id"]] = Satelite(id=row["sat_id"])

            self.satelites[row["sat_id"]].datos.append(self._map_datos(row))
            
        self._print_data()
        return list(self.satelites.values())
    
    def _calcular_segundos(self, hora: str) -> int:
        hora_time = time.fromisoformat(hora)
        return hora_time.hour * 3600 + hora_time.minute * 60 + hora_time.second
    
    def _map_datos(self, row: pd.Series) -> DatosSatelite:
        return DatosSatelite(
            segundo=self._calcular_segundos(row["hora"]),
            prx=round(row["PRx"], 2),
            is_visible_outer=row["is_visible_outer"],
            is_visible_inner=row["is_visible_inner"]
        )

    def _print_data(self) -> None:
        for satelite in self.satelites.values():
            print(f"Satélite ID: {satelite.id}")
            print(f"Cantidad de datos: {len(satelite.datos)}")
            count_outer_visible = sum(1 for datos in satelite.datos if datos.is_visible_outer)
            print(f"Cantidad de datos con is_visible_outer=True: {count_outer_visible}")
            count_inner_visible = sum(1 for datos in satelite.datos if datos.is_visible_inner)
            print(f"Cantidad de datos con is_visible_inner=True: {count_inner_visible}")
