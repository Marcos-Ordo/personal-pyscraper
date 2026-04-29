from abc import ABC, abstractmethod

class ProductScraper(ABC):

    def __init__(self):
        pass
    
    @abstractmethod
    def scrap(self, id):
        """
        PROP: Esta función retorna una tupla con el nombre del producto y su precio.
        PREC: 
            * Debe ser posible conectarse a la "target website".
            * Cada subclase puede tener más precondiciones para este methodo.
        """
        pass