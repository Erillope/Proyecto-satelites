from datos_satelites import Satelite, DatosSatelite
import matplotlib.pyplot as plt
import numpy as np
from typing import Callable

class GraficadorPotencia:

    def __init__(self, satelites: list[Satelite]):
        self.satelites = satelites

    def grafica_potencias(self, grafica_name="grafica_potencias.png") -> None:
        plt.figure(figsize=(10, 6))
        for satelite in self.satelites:
            segundos = [dato.segundo for dato in satelite.datos]
            prx_values = [dato.prx for dato in satelite.datos]
            
            horas_str = [f"{segundo // 3600:02d}:{(segundo % 3600) // 60:02d}:{segundo % 60:02d}" for segundo in segundos]

            step = max(1, len(segundos) // 10)
            plt.xticks(
                segundos[::step],
                horas_str[::step]
            )

            plt.plot(segundos, prx_values, label=f'Satélite {satelite.id}')
        
        self._show_plot('Potencia de Señal de Satélites', 'Horas', 'PRx', grafica_name)
    
    def grafica_disponibilidad_cobertura(self, grafica_name="grafica_disponibilidad_cobertura.png") -> None:
        plt.figure(figsize=(10, 6))
        segundos = [dato.segundo for dato in self.satelites[0].datos]
        disponibilidad_outer = self._obtener_disponibilidad(segundos, lambda dato: dato.is_visible_outer)
        disponibilidad_inner = self._obtener_disponibilidad(segundos, lambda dato: dato.is_visible_inner)
        
        str_times = [f"{segundo // 3600:02d}:{(segundo % 3600) // 60:02d}:{segundo % 60:02d}" for segundo in segundos]
        plt.xticks([i for i in range(0, len(segundos), max(1, len(segundos) // 10))], [str_times[i] for i in range(0, len(segundos), max(1, len(segundos) // 10))])
        
        disponibilidad_outer = np.array(disponibilidad_outer)
        disponibilidad_outer_0 = np.where(disponibilidad_outer == 0, 0, np.nan)
        disponibilidad_outer_1 = np.where(disponibilidad_outer == 1, 0, np.nan)

        disponibilidad_inner = np.array(disponibilidad_inner)
        disponibilidad_inner_0 = np.where(disponibilidad_inner == 0, 1, np.nan)
        disponibilidad_inner_1 = np.where(disponibilidad_inner == 1, 1, np.nan)

        plt.plot(segundos, disponibilidad_outer_0, 'red', label='No Disponible (Outer)')
        plt.plot(segundos, disponibilidad_outer_1, 'green', label='Disponible (Outer)')

        plt.plot(segundos, disponibilidad_inner_0, 'orange', label='No Disponible (Inner)')
        plt.plot(segundos, disponibilidad_inner_1, 'blue', label='Disponible (Inner)')
        
        self._show_plot('Disponibilidad Cobertura', 'Horas', 'Disponibilidad', grafica_name)
    
    def _obtener_disponibilidad(self, segundos: list[int], condition: Callable[[DatosSatelite], bool]) -> list[int]:
        disponibilidad = []
        for segundo in segundos:
            for satelite in self.satelites:
                if any(dato.segundo == segundo and condition(dato) for dato in satelite.datos):
                    disponibilidad.append(1)
                    break
            else:
                disponibilidad.append(0)
        return disponibilidad

    def _show_plot(self, title: str, xlabel: str, ylabel: str,  grafica_name: str) -> None:
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid()
        plt.savefig(grafica_name)
        plt.show()