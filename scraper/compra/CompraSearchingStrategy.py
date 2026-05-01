from abc                       import ABC, abstractmethod
from scraper.SearchingStrategy import SearchingStrategy

class CompraSearchingStrategy(SearchingStrategy, ABC):
    """
    Esta clase define a search como un template donde sus subclases tienen que proveer el hook para usarlo
    Metodos:
        * search(msg): Este metodo se encarga de buscar por todo el data del adapter los productos que cumplan con el hook para guardarlos en la memoria del scraper
        * condition_hook(msg, product): Es abstracto
    """
    def __init__(self, scraper):
        super().__init__(scraper)
    
    def search(self, msg: str):
        """
        Proposito: Este metodo se encarga de buscar por todo el data del adapter los productos que cumplan con el hook para guardarlos en la memoria del scraper
        """
        if msg != None:
            for product in self.scraper.adapter.data:
                if self.condition_hook(msg, product):
                    self.scraper.memory.add(self.scraper.standarize_item(product, msg))

    @abstractmethod
    def condition_hook(self, msg, product) -> bool:
        pass


class CompraSearchByMessage(CompraSearchingStrategy):
    """
    Esta clase define el hook de la superclase
    Metodo:
        * condition_hook(msg, product): Este metodo verifica que el nombre del producto dado contenga el mensaje dado
    """
    def condition_hook(self, msg, product) -> bool:
        """
        Proposito: Este metodo verifica que el nombre del producto dado contenga el mensaje dado
        """
        return msg in product.value["nombre"]


class CompraSearchingDefaults(CompraSearchingStrategy, ABC):
    """
    Esta clase define el hook de la superclase default para sus subclases
    Metodo:
        * condition_hook(msg, product): Este metodo verifica que el nombre del producto dado empiece con el mensaje dado
    """
    def __init__(self, scraper):
        super().__init__(scraper)

    def condition_hook(self, msg, product) -> bool:
        """
        Proposito: Este metodo verifica que el nombre del producto dado empiece con el mensaje dado
        """
        return product.value["nombre"].startswith(msg)


class CompraSearchingCPUs(CompraSearchingDefaults):
    """
    Esta clase solo redefine el metodo search
    Metodo:
        * search(): Se redefine para que utilice el search() de su superclase con el mensaje "Procesador"
    """
    def search(self, msg):
        """
        Proposito: Se redefine para que utilice el search() de su superclase con el mensaje "Procesador"
        """
        super().search("Procesador")


class CompraSearchingGPUs(CompraSearchingDefaults):
    """
    Esta clase solo redefine el metodo search
    Metodo:
        * search(): Se redefine para que utilice el search() de su superclase con el mensaje "Placa de video"
    """
    def search(self, msg):
        """
        Proposito: Se redefine para que utilice el search() de su superclase con el mensaje "Placa de video".
        """
        super().search("Placa de Video")
