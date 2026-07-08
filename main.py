from repository import RepositorioSatelites, Satelite
from graficador import GraficadorCurvasPotencias, GraficadorHandover
from handover import Handover
import numpy as np

MIN_ELEVATION_DEG = 10
MIN_PRX = 7
HANDOVER_THRESHOLD = 8

repositorio_satelites = RepositorioSatelites(excel_file="datos6.xlsx")
repositorio_satelites.generate_log("satelites_log.txt")

time_range = repositorio_satelites.satelites_tiempo_real.time_range

graficador_potencias = GraficadorCurvasPotencias()
graficador_filtro_1 = GraficadorCurvasPotencias()
graficador_filtro_2 = GraficadorCurvasPotencias()
graficador_filtro_3 = GraficadorCurvasPotencias()

graficador_handover = GraficadorHandover()
handover = Handover(threshold=HANDOVER_THRESHOLD)
muestras_prx = []
current_sat: Satelite | None = None

for t in time_range:
    satelites = repositorio_satelites.find_by_time(t)
    graficador_potencias.add_all_curvas(satelites, t)

    satelites = [s for s in satelites if s.is_visible_outer]
    graficador_filtro_1.add_all_curvas(satelites, t)

    satelites = [s for s in satelites if s.elevacion_deg > MIN_ELEVATION_DEG]
    graficador_filtro_2.add_all_curvas(satelites, t)

    satelites = [s for s in satelites if s.prx > MIN_PRX]
    graficador_filtro_3.add_all_curvas(satelites, t)
    
    current_sat = handover.execute(current_sat, satelites, t)
    if current_sat is not None:
        muestras_prx.append(current_sat.prx)
    else:
        muestras_prx.append(np.nan)

handover.generate_log("handover_log.txt")

graficador_potencias.plot("curvas_potencias")
graficador_filtro_1.plot("curvas_filtro_1")
graficador_filtro_2.plot("curvas_filtro_2")
graficador_filtro_3.plot("curvas_filtro_3")
graficador_handover.plot(handover.critical_points, time_range, muestras_prx, "curva_handover")