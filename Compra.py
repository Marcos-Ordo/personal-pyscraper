'''
    target page: https://compragamer.com/
'''

import Scraper
import csv

MICROS = "https://compragamer.com/productos?agrup=7"
PLACAS = "https://compragamer.com/productos?agrup=2"

'''
Interfaz: redo_data(self); search_for(self,search)
'''

class Compra(Scraper.Scraper):
    def __init__(self):
        super().__init__("https://compragamer.com/", True)
        with open('data.csv', mode='a', newline='') as output_file:
            data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_csv.writerow(['Compragamer', ''])
            data_csv.writerow(['Artículo', 'Precio'])
        # Guardo en page_data la información que voy a utilizar.
        self.page_data = [
            "ng-star-inserted", "cgw-product-card", # [0,1] = Box
            "cg__fw-400 mb-5 product-card__title ng-star-inserted", "h3", # [2,3] = Description
            "txt_price", "span" # [4,5] = Price
        ]

    # PROPÓSITO: borra los datos que ya están en el csv y vuelve a escribir los titulos de la sección.
    def redo_data(self):
        Scraper.delete_data()
        with open('data.csv', mode='w', newline='') as output_file:
            data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_csv.writerow(['Compragamer', ''])
            data_csv.writerow(['Artículo', 'Precio'])

    # PROPÓSITO: Buscar !search en la barra de busqueda de la página.
    def search_for(self, search):
        super().search_for(search,'//input[@id="mat-input-0"]')