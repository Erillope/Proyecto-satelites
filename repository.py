from pydantic import BaseModel, Field
from datetime import time
from typing import List, Dict, ClassVar, Tuple
import pickle
from pathlib import Path
import pandas as pd
import random

SateliteID = str

class Satelite(BaseModel):
    id: SateliteID
    prx: float = 0.0
    is_visible_outer: bool = False
    is_visible_inner: bool = False
    elevacion_deg: float = 0
    color: str = Field(default_factory=lambda: "#{:06x}".format(random.randint(0, 0xFFFFFF)))

    def set_prx(self, prx: float) -> None:
        self.prx = prx

class CacheSatelitesTiempoReal(BaseModel):
    data: Dict[time, List[Satelite]] = {}
    time_range: List[time] = []
    
    def add_satelites(self, hora: time, satelite: Satelite) -> None:
        if hora not in self.data:
            self.data[hora] = []
        self.data[hora].append(satelite)

class RepositorioSatelites:
    COLUMNS: ClassVar[List[str]] = ["hora", "sat_id", "PRx", "is_visible_outer", "is_visible_inner", "elevacion_deg"]

    def __init__(self, excel_file: str) -> None:
        self.excel_file = excel_file
        self.cache_file = excel_file.replace(".xlsx", "_cache.pkl")
        self.satelites_tiempo_real = self._init_cache()

    def find_by_time(self, time: time) -> List[Satelite]:
        return self.satelites_tiempo_real.data.get(time, [])
    
    def _init_cache(self) -> CacheSatelitesTiempoReal:
        satelites_tiempo_real: CacheSatelitesTiempoReal
        if Path(self.cache_file).exists():
            print(f"Cargando datos de satélites desde el archivo de caché: {self.cache_file}")
            with open(self.cache_file, "rb") as f:
                satelites_tiempo_real = pickle.load(f)
        else:
            print(f"No se encontró el archivo de caché: {self.cache_file}. Inicializando desde el archivo Excel: {self.excel_file}")
            satelites_tiempo_real = self._init_from_excel()
            with open(self.cache_file, "wb") as f:
                pickle.dump(satelites_tiempo_real, f)
        return satelites_tiempo_real
    
    def _init_from_excel(self) -> CacheSatelitesTiempoReal:
        df = pd.read_excel(self.excel_file, usecols=self.COLUMNS)
        time_range = sorted(df["hora"].apply(time.fromisoformat).unique())
        satelites_tiempo_real = CacheSatelitesTiempoReal(time_range=time_range)

        for i, row in df.iterrows():
            print(f"Procesando fila numero {i}")
            hora = time.fromisoformat(row["hora"])
            satelite = self._map_satelite(row)
            satelites_tiempo_real.add_satelites(hora, satelite)

        return satelites_tiempo_real
    
    def _map_satelite(self, row: pd.Series) -> Satelite:
        return Satelite(
            id=row["sat_id"],
            prx=round(row["PRx"], 2),
            is_visible_outer=row["is_visible_outer"],
            is_visible_inner=row["is_visible_inner"],
            elevacion_deg=row["elevacion_deg"]
        )

    def generate_log(self, log_file: str) -> None:
        count_data = self._count_inners_outers()
        with open(log_file, "w", encoding="utf-8") as f:
            for sat_id in count_data:
                inner_count, outer_count = count_data[sat_id]
                f.write(f"Satelite ID: {sat_id}\n")
                f.write(f"Cantidad de datos con is_visible_inner=True: {inner_count}\n")
                f.write(f"Cantidad de datos con is_visible_outer=True: {outer_count}\n")

    
    def _count_inners_outers(self) -> Dict[SateliteID, Tuple[int, int]]:
        count_dict: Dict[SateliteID, Tuple[int, int]] = {}

        for _, satelites_list in self.satelites_tiempo_real.data.items():
            for satelite in satelites_list:
                if satelite.id not in count_dict:
                    count_dict[satelite.id] = (0, 0)
                inner_count, outer_count = count_dict[satelite.id]
                if satelite.is_visible_inner:
                    inner_count += 1
                if satelite.is_visible_outer:
                    outer_count += 1
                count_dict[satelite.id] = (inner_count, outer_count)
        return count_dict
        