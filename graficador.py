from datos_satelites import Satelite
import matplotlib.pyplot as plt

class GraficadorPotencia:

    def grafica_potencias(self, satelites: list[Satelite], grafica_name="grafica_potencias.png") -> None:
        plt.figure(figsize=(10, 6))
        for satelite in satelites:
            segundos = [dato.segundo for dato in satelite.datos]
            prx_values = [dato.prx for dato in satelite.datos]
            plt.plot(segundos, prx_values, label=f'Satélite {satelite.id}')
        
        self._show_plot('Potencia de Señal de Satélites', grafica_name)
    
    def grafica_potencias_filtro1(self, satelites: list[Satelite], grafica_name="grafica_potencias_filtro1.png") -> None:
        plt.figure(figsize=(10, 6))
        for satelite in satelites:
            segundos = [dato.segundo for dato in satelite.datos if dato.is_visible_outer]
            prx_values = [dato.prx for dato in satelite.datos if dato.is_visible_outer]
            plt.plot(segundos, prx_values, label=f'Satélite {satelite.id}')
        
        self._show_plot('Potencia de Señal de Satélites (Filtro 1)', grafica_name)

    def _show_plot(self, title: str, grafica_name: str) -> None:
        plt.title(title)
        plt.xlabel('Segundos')
        plt.ylabel('PRx')
        plt.legend()
        plt.grid()
        plt.savefig(grafica_name)
        plt.show()