from abc import ABC, abstractmethod

class ProductScraper(ABC):

    def __init__(self, id):
        self.__id = id

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id):
        self.__id = id
    
    @abstractmethod
    def scrap(self) -> dict:
        """
        PROP: Esta función retorna una tupla con el nombre del producto y su precio.
        PREC: 
            * Debe ser posible conectarse a la "target website".
            * Cada subclase puede tener más precondiciones para este methodo.
        """
        pass