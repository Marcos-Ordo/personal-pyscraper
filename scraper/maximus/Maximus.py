### Target website: https://www.maximus.com.ar/

import requests
import json

from scraper.Scraper                          import Item, Scraper, ProductScraper
from scraper.maximus.MaximusSearchingStrategy import MaximusSearchingCPUs, MaximusSearchingGPUs, MaximusSearchByMessage

HOME   = "https://www.maximus.com.ar/"

class Maximus(Scraper):
    """
    Esta clase se encarga de ser el scraper de la tienda Maximus. Define 2 propiedades que utilizan sus estrategias, un metodo para elegir entre esas estrategias y un metodo para estandarizar Items en base al dict recibido por su adapter
    Metodo:
        * change_strat_to(strategy): Cambia la estrategia a la estrategia dada. Recibe las estrategias "cpu", "gpu" y "msg"
        * standarize_item(item, product_type): Estandariza el dict dentro del item a guardar y lo etiqueta con el origen y el tipo de producto
    Propiedades: 
        * adapter: Es el adaptador que mediante parametros genera respuestas de la "target website"
        * productScraper: Es un scraper de un producto individual
    """
    def __init__(self):
        super().__init__()
        self.__adapter        = MaximusAdapter()
        self.__productScraper = MaximusProductScraper(self.adapter)

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
            case "cpu": self.searchingStrategy = MaximusSearchingCPUs(self)
            case "gpu": self.searchingStrategy = MaximusSearchingGPUs(self)
            case "msg": self.searchingStrategy = MaximusSearchByMessage(self)
            case _    : pass

    def standarize_item(self, item, product_type):
        """
        Proposito: Estandariza el dict dentro del item a guardar y lo etiqueta con el origen y el tipo de producto
        """
        temp = {}
        temp['id']     = item.value['item_id']
        temp['name']   = item.value['item_desc']
        temp['price']  = item.value['prli_price_original']
        temp['origin'] = "Maximus"
        temp['type']   = product_type
        return Item(temp, 'id')



class MaximusProductScraper(ProductScraper):
    """
    Esta clase se encarga de scrapear solo 1 producto con una id dada
    Metodo:
        * scrap: Esta función retorna un dict con todos los datos del producto apartir de la "target website", si no puede retorna None
    Atributo:
        * adapter: Almacena el adapter para buscar los datos
    """
    def __init__(self, adapter: MaximusAdapter):
        super().__init__()
        self.__adapter = adapter

    @property
    def adapter(self):
        return self.__adapter

    def scrap(self, id) -> None | Item:
        """
        Proposito: Esta función retorna un dict con todos los datos del producto apartir de la "target website", si no puede retorna None
        """
        result = self.adapter.request({'item_id': id})

        if result == None:
            return None
        else:
            return Item(result, 'item_id')


class MaximusAdapter():
    """
    Esta clase se encarga de realizar las requests para los distintos componentes del Scraper principal
    Metodos:
        * request(params, session = request.Session()): 
            Proposito: Es la funcion que se encarga de crear una sesion para hacer requests, crea los headers, el payload y algunos params genericos para generar una response que despues retorna, si no puede hacer la request porque no tiene conexion o porque el json del POST queda mal retorna None
        * __prettify_data(json_data):
            Proposito: Esta funcion recibe los datos de la respuesta en json y los trabaja, si en esa respuesta no está el campo 'd' y dentro del campo 'd' hay un objeto json con el campo 'data' retorna None
        * __guid(cookies):
            Proposito: Esta funcion recibe una lista de cookies y retorna el 'guid' de la pagina en base a una de ellas, si la cookie con la 'guid' no está retorna None
    """
    def __init__(self):
        pass

    def request(self, params: dict, session = requests.Session()) -> None | dict: # Moví la sessión aca pq necesitaba mockear la sesion fuera del metodo
        """
        Proposito: Es la funcion que se encarga de crear una sesion para hacer requests, crea los headers, el payload y algunos params genericos para generar una response que despues retorna, si no puede hacer la request porque no tiene conexion o porque el json del POST queda mal retorna None
        """
        session.get(HOME)
        guid = self.__guid(session.cookies)

        if guid != None:
            # Esta URL es la url de la API de Maximus. es donde hago la consulta para obtener la info del producto.
            url = "https://www.maximus.com.ar/wfmWebSite2.aspx/wsNRW_Script"

            headers = {
                "accept":       "*/*",
                "content-type": "application/json; charset=UTF-8",
                "origin":       "https://www.maximus.com.ar",
                "referer":      "https://www.maximus.com.ar/",
                "user-agent":   "Mozilla/5.0",
            }
            # Estos valores no se a que se refieren pero parecen no cambiar!
            params["prli_id"] = 17
            params["comp_id"] = 1
            params["ws_id"]   = guid
            params["cust_id"] = -1

            payload = {
                "guidWS_Id":      guid,
                "strScriptLabel": "web.MAX.GetItemList4Search_v3",
                "JSonParameters": json.dumps(params)
            }

            response = session.post(
                url,
                headers=headers,
                json=payload
            )
            code = response.status_code
            if code < 200 or code > 299:
                return None
            else:
                input = json.loads(response.text)
                data  = self.__prettify_data(input)
                return(data)
        else:
            return None
    
    def __prettify_data(self, json_data) -> None | dict:
        """
        Proposito: Esta funcion recibe los datos de la respuesta en json y los trabaja, si en esa respuesta no está el campo 'd' y dentro del campo 'd' hay un objeto json con el campo 'data' retorna None
        """
        try:
            return json.loads(json_data['d'])['data']
        except:
            pass
        return None
    
    def __guid(self, cookies) -> None | str:
        """
        Proposito: Esta funcion recibe una lista de cookies y retorna el 'guid' de la pagina en base a una de ellas, si la cookie con la 'guid' no está retorna None
        """
        for cookie in cookies:
            if cookie.name.startswith("GBP_") and cookie.name != "GBP_":
                return cookie.name.replace("GBP_", "")
        return None
