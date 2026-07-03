from datos_satelites import XLSXLectorSatelite
from graficador import GraficadorPotencia
from filtro_potencia import FiltroFootprintExterno, FiltroPoteciaRecibida

lector = XLSXLectorSatelite("datos4.xlsx")
satelites = lector.read_data()

filtro_1 = FiltroFootprintExterno()

filtro_2 = FiltroPoteciaRecibida(sensibilidad=7)


filtro_1.next(filtro_2)

satelites_filtrados = filtro_1.filtrar(satelites)

graficador = GraficadorPotencia(satelites_filtrados)

graficador.grafica_potencias(grafica_name="grafica_potencias_filtro_potencia_recibida.png")