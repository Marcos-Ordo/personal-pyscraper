'''
    Target page: https://www.maximus.com.ar/

    Interfaz: 
        ?
'''

from scraper.Scraper        import *
from scraper.ProductScraper import *
import requests
import json
import re
# import csv

HOME   = "https://www.maximus.com.ar/"
MICROS = "https://www.maximus.com.ar/Productos/Microprocesadores/maximus.aspx?/CAT=52/SCAT=-1/M=-1/OR=1/PAGE=1/"
PLACAS = "https://www.maximus.com.ar/Productos/Placas-De-Video/maximus.aspx?/CAT=48/SCAT=-1/M=-1/OR=1/PAGE=1/"

class Maximus(Scraper):
    def __init__(self): #Temporalmente le doy la id manualmente al crearlo
        super().__init__()

        # Genero el csv donde guardar la información más tarde.
        # with open('data.csv', mode='a', newline='') as output_file:
        #     data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     data_csv.writerow(['Maximus', ''])
        #     data_csv.writerow(['Artículo', 'Precio'])

    def search_gpus(self):
        items = self.__search_gpu_in_page(1)
        i = 1
        while len(items) > 0:
            for item in items:
                item = {k: v for k, v in item if k not in ['item_id','item_desc','prli_price_original']}
                self.memory.append(item)
            i += 1
            items = self.__search_gpu_in_page(i)

    def __search_gpu_in_page(self, page):
        params = {
            "page": page,
            "cat_id":48,
            "subcat_id":-1,
            "local":0,
            "search":"",
            "order": 1,
            "price_min":"",
            "price_max":"",
            "wco_tV":[]
        }
        return ADAPTER.request(params)

    def _Scraper__scrap_product_with_id(self, id):
        return MaximusProductScraper(id).scrap()

class MaximusProductScraper(ProductScraper):
    def __init__(self, id):
        super().__init__(id)

    def scrap(self):
        params = {
            "item_id": self.id,
        }
        return ADAPTER.request(params)

# Separate Functions
class MaximusAdapter():
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