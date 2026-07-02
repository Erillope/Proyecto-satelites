from datos_satelites import XLSXLectorSatelite
from graficador import GraficadorPotencia

lector = XLSXLectorSatelite("datos.xlsx")
satelites = lector.read_data()

graficador = GraficadorPotencia()

graficador.grafica_potencias_filtro1(satelites)