from abc import ABC, abstractmethod
from datos_satelites import Satelite

class FiltroPotencia(ABC):

    def __init__(self):
        self._next_filtro: FiltroPotencia | None = None

    @abstractmethod
    def filtrar(self, satelites: list[Satelite]) -> list[Satelite]: ...

    def next(self, next_filtro: 'FiltroPotencia') -> 'FiltroPotencia':
        self._next_filtro = next_filtro
        return next_filtro


class FiltroFootprintExterno(FiltroPotencia):
    def __init__(self):
        super().__init__()

    def filtrar(self, satelites: list[Satelite]) -> list[Satelite]:
        satelites_filtrados: list[Satelite] = []

        for satelite in satelites:
            datos_satelite = [dato for dato in satelite.datos if dato.is_visible_outer]
            if len(datos_satelite) > 0:
                satelites_filtrados.append(Satelite(id=satelite.id, datos=datos_satelite))
        
        if self._next_filtro:
            return self._next_filtro.filtrar(satelites_filtrados)
        return satelites_filtrados


class FiltroPoteciaRecibida(FiltroPotencia):
    def __init__(self, sensibilidad: float):
        super().__init__()
        self.sensibilidad = sensibilidad

    def filtrar(self, satelites: list[Satelite]) -> list[Satelite]:
        satelites_filtrados: list[Satelite] = []

        for satelite in satelites:
            datos_satelite = [dato for dato in satelite.datos if dato.prx >= self.sensibilidad]
            if len(datos_satelite) > 0:
                satelites_filtrados.append(Satelite(id=satelite.id, datos=datos_satelite))
        
        if self._next_filtro:
            return self._next_filtro.filtrar(satelites_filtrados)
        return satelites_filtrados