'''
    target page: https://compragamer.com/

    Interfaz: 
        redo_data(self); 
        search_for(self,search)
'''

from scraper.Scraper import *
# import csv

HOME   = "https://www.compragamer.com/"
MICROS = "https://www.compragamer.com/productos?agrup=7"
PLACAS = "https://www.compragamer.com/productos?agrup=2"

class Compra(Scraper):
    def __init__(self):
        super().__init__()
        
        # with open('data.csv', mode='a', newline='') as output_file:
        #     data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     data_csv.writerow(['Compragamer', ''])
        #     data_csv.writerow(['Artículo', 'Precio'])
        # Guardo en page_data la información que voy a utilizar.

    def __scrap_product_with_id(self, id):
        pass