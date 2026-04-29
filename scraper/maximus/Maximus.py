### Target website: https://www.maximus.com.ar/

import requests
import json

from scraper.Scraper                          import Scraper, ProductScraper
from scraper.maximus.MaximusSearchingStrategy import MaximusSearchingCPUs, MaximusSearchingGPUs, MaximusSearchByMessage

HOME   = "https://www.maximus.com.ar/"

class Maximus(Scraper):
    """
    Esta clase se encarga de ser el scraper de la tienda Maximus. Define 2 propiedades que utilizan sus estrategias y un metodo para elegir entre esas estrategias
    Metodo:
        * changeStratTo(strategy): Cambia la estrategia a la estrategia dada. Recibe las estrategias "cpu", "gpu" y "msg"
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
    
    def changeStratTo(self, strategy):
        match strategy.lower():
            case "cpu": self.searchingStrategy = MaximusSearchingCPUs(self)
            case "gpu": self.searchingStrategy = MaximusSearchingGPUs(self)
            case "msg": self.searchingStrategy = MaximusSearchByMessage(self)
            case _    : pass

class MaximusProductScraper(ProductScraper):
    """
    Esta clase se encarga de scrapear solo 1 producto con una id dada.
    Interfaz:
        * scrap:
            Proposito: scrapear la pagina del producto con la id que tiene al inicializarse una instancia.
            Precondicion: Debe haber conexion con la "target website".
    """
    def __init__(self, adapter):
        super().__init__()
        self.__adapter = adapter

    @property
    def adapter(self):
        return self.__adapter

    def scrap(self, id):
        # Precondicion: Solo funciona mientras sea posible conectarse a la "target website"
        params = {
            "item_id": id,
        }
        return self.adapter.request(params)


class MaximusAdapter():
    """
    Esta clase se encarga de realizar las requests para los distintos componentes del Scraper principal.
    Interfaz:
        * request: 
            Proposito: Es la funcion que se encarga de crear una sesion para hacer requests, crea los headers, el payload y algunos params genericos para generar una response que despues retorna.
            Precondicion: Debe haber conexion con la "target website".
    """
    def __init__(self):
        pass

    def request(self, params: dict, session = requests.Session()):
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
                raise Exception(f"networkError: {code}")
            else:
                input = json.loads(response.text)
                data  = self.__prettify_data(input)
                return(data)
        else:
            raise Exception("scrapError: couldn't find the guid")
    
    def __prettify_data(self, json_data) -> None | dict:
        """
        Proposito: Esta funcion extrae los datos de la respuesta en json de la pagina, si en esa respuesta no está el campo 'd' y dentro del campo 'd' hay un objeto json con el campo 'data' retorna None
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
