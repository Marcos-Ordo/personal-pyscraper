from abc import ABC, abstractmethod

class Scraper():
    '''
    Esta clase define la propiedad de la memoria de un scraper y la logica para redireccionar una busqueda:
    Metodos: 
        * search(msg): Una funcion que utiliza las distintas estrategias de cada scraper para obtener los productos de cada pagina. Utiliza un parametro para aquellas estrategias que lo necesiten
    Propiedades:
        * memory: Un set con los diccionarios de cada producto
        * 
    '''
    def __init__(self):
        self.__memory            = set()
        self.__searchingStrategy = EmptySearchingStrategy(self)

    @property
    def memory(self):
        return self.__memory

    @property
    def searchingStrategy(self):
        return self.__searchingStrategy
    
    @searchingStrategy.setter
    def searchingStrategy(self, strategy):
        self.__searchingStrategy = strategy

    def search(self, msg = None):
        self.searchingStrategy.search(msg)

    @abstractmethod
    def changeStratTo(self, strategy):
        pass

class Item:
    """
    Esta clase es un wrapper, lo hice para que 2 items puedan compararse por igualdad, asi pueda ponerlos de forma segura en un set.
    Es una clase sin metodos, solo tiene propiedades.
    """
    def __init__(self, value):
        self.__value = value

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.__value['item_id'] == other.__value['item_id']

    def __hash__(self):
        return hash(self.__value['item_id'])

    def __repr__(self):
        return f"ById({self.__value})"
    
    @property
    def value(self):
        return self.__value


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