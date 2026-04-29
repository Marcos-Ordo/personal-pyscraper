### Target website: https://www.maximus.com.ar/

from scraper.Scraper        import *
from scraper.ProductScraper import *
import requests
import json
# import csv

HOME   = "https://www.maximus.com.ar/"
MICROS = "https://www.maximus.com.ar/Productos/Microprocesadores/maximus.aspx?/CAT=52/SCAT=-1/M=-1/OR=1/PAGE=1/"
PLACAS = "https://www.maximus.com.ar/Productos/Placas-De-Video/maximus.aspx?/CAT=48/SCAT=-1/M=-1/OR=1/PAGE=1/"

class Maximus(Scraper):
    """
    Esta clase se encarga de ser el scraper de la tienda Maximus. Utiliza al Adapter y al ProductScraper para funcionar.
    Interfaz:
        * search_gpus:
            Proposito: Scrapea todas las ventanas de gpus.
            Precondicion: Debe haber conexion con la "target website".
        * search_cpus:
            Proposito: Scrapea todas las ventanas de cpus.
            Precondicion: Debe haber conexion con la "target website".
    """
    def __init__(self): #Temporalmente le doy la id manualmente al crearlo
        super().__init__()

        # Genero el csv donde guardar la información más tarde.
        # with open('data.csv', mode='a', newline='') as output_file:
        #     data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     data_csv.writerow(['Maximus', ''])
        #     data_csv.writerow(['Artículo', 'Precio'])

    def search_gpus(self):
        self.__generic_search(self.__search_gpu_in_page)

    def __search_gpu_in_page(self, page):
        return self.__generic_params(page, 48)

    def search_cpus(self):
        self.__generic_search(self.__search_cpu_in_page)

    def __search_cpu_in_page(self, page):
        return self.__generic_params(page, 52)

    # GENERICS
    def __generic_search(self, func):
        items = func(1)
        i = 1
        while len(items) > 0:
            for item in items:
                temp = ById({key: item[key] for key in ['item_id','item_desc','prli_price_original']})
                self.memory.add(temp)
            i += 1
            items = func(i)

    def __generic_params(self, page, cat):
        params = {
            "page":      page,
            "cat_id":    cat,
            "subcat_id": -1,
            "local":     0,
            "search":    "",
            "order":     1,
            "price_min": "",
            "price_max": "",
            "wco_tV":    []
        }
        return ADAPTER.request(params)['items']

class MaximusProductScraper(ProductScraper):
    """
    Esta clase se encarga de scrapear solo 1 producto con una id dada.
    Interfaz:
        * scrap:
            Proposito: scrapear la pagina del producto con la id que tiene al inicializarse una instancia.
            Precondicion: Debe haber conexion con la "target website".
    """
    def __init__(self, id):
        super().__init__(id)

    def scrap(self):
        # Precondicion: Solo funciona mientras sea posible conectarse a la "target website"
        params = {
            "item_id": self.id,
        }
        return ADAPTER.request(params)


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

    def request(self, params: dict):
        session = requests.Session()
        session.get(HOME)
        guid = self.__maybe_guid(session)

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
    
    def __prettify_data(self, data):
        temp1 = json.loads(data['d'])
        resul = temp1['data']
        return resul
    
    def __maybe_guid(self, session: requests.Session) -> None | str: 
            guid = None
            for cookie in session.cookies:
                if cookie.name.startswith("GBP_") and cookie.name != "GBP_":
                    guid = cookie.name.replace("GBP_", "")
                    break
            return guid
    
ADAPTER = MaximusAdapter()