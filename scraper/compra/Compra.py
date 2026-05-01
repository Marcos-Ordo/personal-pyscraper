### target website: https://compragamer.com/

import requests
import json

from scraper.Scraper                        import Item, Scraper, ProductScraper
from scraper.compra.CompraSearchingStrategy import CompraSearchByMessage, CompraSearchingCPUs, CompraSearchingGPUs

class Compra(Scraper):
    """
    Esta clase se encarga de ser el scraper de la tienda Compragamer. Define 2 propiedades que utilizan sus estrategias, un metodo para elegir entre esas estrategias y un metodo para estandarizar Items en base al dict recibido por su adapter
    Metodo:
        * change_strat_to(strategy): Cambia la estrategia a la estrategia dada. Recibe las estrategias "cpu", "gpu" y "msg"
        * standarize_item(item, product_type): Estandariza el dict dentro del item a guardar y lo etiqueta con el origen y el tipo de producto
    Propiedades: 
        * adapter: Es el adaptador que mediante parametros genera respuestas de la "target website"
        * productScraper: Es un scraper de un producto individual
    """
    def __init__(self):
        super().__init__()
        self.__adapter        = CompraAdapter()
        self.__productScraper = CompraProductScraper(self.__adapter)

        self.__adapter.request()

    @property
    def adapter(self):
        return self.__adapter
    
    @property
    def productScraper(self):
        return self.__productScraper

    def change_strat_to(self, strategy) -> None:
        """
        Proposito: Cambia la estrategia a la estrategia dada. Recibe las estrategias "cpu", "gpu" y "msg"
        """
        match strategy.lower():
            case "cpu": self.searchingStrategy = CompraSearchingCPUs(self)
            case "gpu": self.searchingStrategy = CompraSearchingGPUs(self)
            case "msg": self.searchingStrategy = CompraSearchByMessage(self)
            case _    : pass

    def standarize_item(self, item, product_type):
        """
        Proposito: Estandariza el dict dentro del item a guardar y lo etiqueta con el origen y el tipo de producto
        """
        temp = {} 
        temp['id']     = item.value["id_producto"]
        temp['name']   = item.value["nombre"]
        temp['price']  = item.value["precioEspecial"]
        temp['origin'] = "Compragamer"
        temp['type']   = product_type
        return Item(temp, 'id')


class CompraProductScraper(ProductScraper):
    """
    Esta clase se encarga de scrapear solo 1 producto con una id dada
    Metodo:
        * scrap: Esta función retorna un Item resultante de buscaren el data del adapter el producto con la id dada. Si no puede retorna None
    Atributo:
        * adapter: Almacena el adapter con los datos
    """
    def __init__(self, adapter: CompraAdapter):
        self.__adapter = adapter
    
    @property
    def adapter(self):
        return self.__adapter
    
    def scrap(self, id) -> None | Item:
        """
        Proposito: Esta función retorna un Item resultante de buscaren el data del adapter el producto con la id dada. Si no puede retorna None
        """
        for product in self.__adapter.data:
            if product.value["id_producto"] == id:
                return product
        return None


class CompraAdapter():
    """
    Esta clase se encarga de realizar las requests para los distintos componentes del Scraper principal
    Metodos:
        * request(): 
            Este metodo se encarga de generar los headers y hacer un get en la url correcta para obtener el json bruto con todos los productos, luego los guarda en un atributo. Si no puede retorna None
        * __save_data(json_data): Este metodo agrega todos los productos del "json_data" al atributo "data" envolviendolos antes en un Item
    Atributo:
        * data: Este atributo almacena en un Set todos los Items obtenidos por request()
    """
    def __init__(self):
        self.__data: set[Item] = set()

    @property
    def data(self):
        return self.__data

    def request(self) -> None:
        """
        Proposito: Este metodo se encarga de generar los headers y hacer un get en la url correcta para obtener el json bruto con todos los productos, luego los guarda en un atributo. Si no puede retorna None
        """
        session = requests.Session()

        headers = {
            "accept":       "application/json, text/plain, */*",
            "content-type": "application/json; charset=UTF-8",
            "origin":       "https://compragamer.com",
            "referer":      "https://compragamer.com/",
            "user-agent":   "Mozilla/5.0",
            "Host":         "static.compragamer.com"
        }

        # Parese que en esta URL está el json con los datos brutos.
        url = "https://static.compragamer.com/productos"

        response = session.get(
            url,
            headers=headers
        )

        code = response.status_code
        if code < 200 or code > 299:
            raise Exception(f"networkError: {code}")
        else:
            input = json.loads(response.text)
            self.__save_data(input)
    
    def __save_data(self, json_data: list[dict]) -> None:
        """
        Proposito: Este metodo agrega todos los productos del "json_data" al atributo "data"
        """
        for item in json_data:
            self.__data.add(Item({k: item[k] for k in ["id_producto","nombre","precioEspecial"]}, "id_producto"))
