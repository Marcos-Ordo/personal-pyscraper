from abc import ABC, abstractmethod

class SearchingStrategy(ABC):
    """
    Esta clase abstracta define un metodo y una propiedad que tienen que tener todas las estrategias de busqueda.
    Metodo: 
        * search(msg): Debe ser capaz de buscar lo que se ingrese por parametro. El parametro puede ser vacío porque hay algunas estrategias que no lo usan
    Propiedad: 
        * scraper: Es el respectivo scraper al que va a ir la informacion que saque la estrategia y ademas provee propiedades utiles para cada estrategia
    """
    def __init__(self, scraper):
        self.__scraper = scraper

    @property
    def scraper(self):
        return self.__scraper

    @abstractmethod
    def search(self, msg):
        pass


class EmptySearchingStrategy(SearchingStrategy):
    """
    Esta clase define una estrategia de busqueda nula. cuando le dicen que busque no hace nada.
    """
    def __init__(self, scraper):
        super().__init__(scraper)

    def search(self, msg):
        pass