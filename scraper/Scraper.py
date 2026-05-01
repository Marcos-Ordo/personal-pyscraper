from abc                       import ABC, abstractmethod
from queue                     import Queue
from scraper.SearchingStrategy import EmptySearchingStrategy
import threading

class Scraper(ABC):
    '''
    Esta clase define la propiedad de la memoria de un scraper y la logica para redireccionar una busqueda:
    Metodos: 
        * search(msg): Una funcion que utiliza las distintas estrategias de cada scraper para obtener los productos de cada pagina. Utiliza un parametro para aquellas estrategias que lo necesiten
        * change_strat_to(strategy): Es Abstracto
        * standarize_item(item, product_type): Es Abstracto
    Propiedades:
        * memory: Es un Memory con los diccionarios de cada producto
        * searchingStrategy: Es la estrategia actual para hacer scraping
    '''
    def __init__(self):
        self.__memory            = Memory()
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
    def change_strat_to(self, strategy) -> None:
        """
        nomenclatura para las diferentes estrategias:
            * cpu: para buscar cpus
            * gpu: para buscar gpus
            * msg: para buscar lo que se envie por parametro
        """
        pass

    @abstractmethod
    def standarize_item(self, item, product_type) -> Item:
        """
        Nomenclatura para un item estandar:
            * id:     id del producto
            * name:   nombre o descripcion del producto
            * price:  precio del producto
            * origin: etiqueta que refencia la pagina de origen del producto
            * type:   etiqueta que referencia el tipo de producto
        """
        pass


class ProductScraper(ABC):
    """
    Esta clase abstracta define un unico metodo para scrapear un unico producto.
    """
    def __init__(self):
        pass
    
    @abstractmethod
    def scrap(self, id) -> Item | None:
        pass


class Memory():
    """
    Esta clase define el comportamiento de una cola FIFO y Set al mismo tiempo, osea define una cola sin repetidos para un único consumidor
    Metodos:
        * add(x): Si tengo permiso del lock y x no está en el historial de elementos, lo agrego al historial y a los movimientos disponibles
        * get(): Retorna todos los movimientos disponibles dejando sin movimientos la memoria
    Atributos:
        * history: Es el conjunto con todos los elementos que pasaron por esta memoria
        * movements: Es una cola que almacena los elementos que estan para consumir
        * lock: Es el Lock que impide que varios objetos agreguen al historial al mismo tiempo
    """
    def __init__(self):
        self.__history   = set()
        self.__movements = Queue()
        self.__lock      = threading.Lock()

    @property
    def lock(self):
        return self.__lock

    def add(self, x):
        """
        Proposito: Si tengo permiso del lock y x no está en el historial de elementos, lo agrego al historial y a los movimientos disponibles
        """
        with self.lock:
            if x not in self.__history:
                self.__history.add(x)
                self.__movements.put(x)
    
    def get(self):
        """
        Proposito: Retorna todos los movimientos disponibles dejando sin movimientos la memoria
        """
        result = []
        while not self.__movements.empty():
            result.append(self.__movements.get())
        return result


class Item:
    """
    Esta clase es un wrapper, lo hice para que 2 items puedan compararse por igualdad, asi pueda ponerlos de forma segura en un set.
    Es una clase sin metodos, solo tiene propiedades.
    Propiedades:
        * eq: define la igualdad en base a la id.
        * hash: define como se puede hashear a un valor unico.
        * repr: define como se representa en la terminal.
        * id_type: define el tipo de id que va a utilizar para compararse.
        * value: define el valor que esta envolviendo.
    """
    def __init__(self, value, id_type):
        self.__id_type = id_type
        self.__value   = value

    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        return self.__value[self.__id_type] == other.value[other.id_type]

    def __hash__(self):
        return hash(self.__value[self.__id_type])

    def __repr__(self):
        return f"Item({self.__value})"
    
    @property
    def id_type(self):
        return self.__id_type

    @property
    def value(self):
        return self.__value
