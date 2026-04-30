from abc                     import ABC, abstractmethod
from scraper.Scraper         import Item, SearchingStrategy

class MaximusSearchingStrategy(SearchingStrategy, ABC):
    """
    Esta clase abstracta define comportamientos genericos para facilitar la busqueda de sus subclases
    Metodos:
        * search(msg): Es abstracto
        * generic_search(func): Define la forma generica de hacer una busqueda, utilizando func para obtener las paginas con los items buscados asi extraerlos, envolverlos en Item y guardarlos en la memoria del scraper
        * generic_check_params(page, cat, bus): Define los parametros genericos para utilizar en el request del adapter
    """
    def __init__(self, scraper):
        super().__init__(scraper)

    @abstractmethod
    def search(self, msg: str):
        pass

    # GENERICS
    def generic_search(self, func):
        """
        Proposito: Define la forma generica de hacer una busqueda, utilizando func para obtener las paginas con los items buscados asi extraerlos, envolverlos en Item y guardarlos en la memoria del scraper
        """
        items = func(1)
        i = 1
        while len(items) > 0:
            for item in items:
                temp = Item({k: item[k] for k in ['item_id','item_desc','prli_price_original']}, 'item_id')
                self.scraper.memory.add(temp)
            i += 1
            items = func(i)

    def generic_check_params(self, page: int, cat: int, bus: str):
        """
        Proposito: Define los parametros genericos para utilizar en el request del adapter
        """
        params = {
            "page":      page,
            "cat_id":    cat,
            "brand_id":  -1,
            "subcat_id": -1,
            "local":     0,
            "search":    bus,
            "order":     1,
            "price_min": "",
            "price_max": "",
            "wco_tV":    []
        }
        return self.scraper.adapter.request(params)['items']
    

class MaximusSearchByMessage(MaximusSearchingStrategy):
    """
    Esta clase define el comportamiento de search para pasar el mensaje
    Metodo:
        * search(msg): Redefine search pasando msg como parametro
    """
    def __init__(self, scraper):
        super().__init__(scraper)

    def search(self, msg = None):
        """
        Proposito: Redefine search pasando msg como parametro
        """
        if msg != None:
            self.generic_search(lambda page: self.generic_check_params(page, -1, msg))
        else:
            pass


class MaximusSearchingDefaults(MaximusSearchingStrategy):
    """
    Esta clase define el comportamiento default para los metodos de busqueda de GPUs y CPUs
    Metodo:
        * search(): Redefine search para que lo unico que tengan que hacer sus subclases es cambiar la categoria
    Atributo:
        * category: Es la categoria del tipo de producto a buscar
    """
    def __init__(self, scraper, category):
        super().__init__(scraper)
        self.__category = category

    @property
    def category(self):
        return self.__category

    def search(self, msg):
        """
        Proposito: Redefine search para que lo unico que tengan que hacer sus subclases es cambiar la categoria
        """
        self.generic_search(lambda page: self.generic_check_params(page, self.category, ""))


class MaximusSearchingCPUs(MaximusSearchingDefaults):
    """
    Esta clase solo le da el valor 52 de categoria (CPUs) a su superclase
    """
    def __init__(self, scraper):
        super().__init__(scraper, 52)


class MaximusSearchingGPUs(MaximusSearchingDefaults):
    """
    Esta clase solo le da el valor 48 de categoria (GPUs) a su superclase
    """
    def __init__(self, scraper):
        super().__init__(scraper, 48)