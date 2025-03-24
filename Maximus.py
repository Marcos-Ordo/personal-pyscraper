'''
    Target page: https://www.maximus.com.ar/
'''

import Scraper
import csv

MICROS = "https://www.maximus.com.ar/Productos/Microprocesadores/maximus.aspx?/CAT=52/SCAT=-1/M=-1/OR=1/PAGE=1/"
PLACAS = "https://www.maximus.com.ar/Productos/Placas-De-Video/maximus.aspx?/CAT=48/SCAT=-1/M=-1/OR=1/PAGE=1/"

'''
Interfaz: get_all(self); redo_data(self); search_for(self,search)
'''

class Maximus(Scraper.Scraper):
    def __init__(self):
        super().__init__("https://www.maximus.com.ar/", True)
        # Genero el csv donde guardar la información más tarde.
        with open('data.csv', mode='a', newline='') as output_file:
            data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_csv.writerow(['Maximus', ''])
            data_csv.writerow(['Artículo', 'Precio'])
        # Guardo en page_data la información que voy a utilizar.
        self.page_data = [
            "product", "div", # [0,1] = Box
            "title-prod", "span", # [2,3] = Description
            "price", "div" # [4,5] = Price
        ]

    # PROPÓSITO: Recibir toda la información relevante de la solapa donde @page está posicionada. 
    # COND: @page debe tener una página.
    def get_all(self):
        super().get_all('//div[@class="button-pager"]/li[last()-1]','//div[@class="col-md-9"]/div[@class="row"]/div[last()]')

    # PROPÓSITO: borra los datos que ya están en el csv y vuelve a escribir los titulos de la sección.
    def redo_data(self):
        Scraper.delete_data()
        with open('data.csv', mode='w', newline='') as output_file:
            data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_csv.writerow(['Maximus', ''])
            data_csv.writerow(['Artículo', 'Precio'])

    # PROPÓSITO: Buscar !search en la barra de busqueda de la página.
    # PARAMS: !search representa un string a buscar.
    def search_for(self, search):
        super().search_for(search,'//input[@class="search-input"]')

## TESTS ##

def test2():
    # OBJETIVO: Testear "get_all", la busqueda en dos paginas diferentes y el guardado de datos.
    m = Maximus()
    input("Press Enter to continue...")
    m.reload_on(MICROS)
    input("Press Enter to continue...")
    m.get_all()
    input("Press Enter to continue...")
    m.show_data()
    input("Press Enter to continue...")
    m.search_for("rtx")
    input("Press Enter to continue...")
    m.get_content()
    input("Press Enter to continue...")
    m.show_data()
    input("Press Enter to continue...")
    m.save_data()
    input("Press Enter to continue...")
    m.destroy()

def test1():
    # OBJETIVO: Testear la busqueda en dos páginas diferentes.
    m = Maximus()
    input("Press Enter to continue...")
    m.reload_on(MICROS)
    input("Press Enter to continue...")
    m.get_content()
    input("Press Enter to continue...")
    m.show_data()
    input("Press Enter to continue...")
    m.search_for("rtx")
    input("Press Enter to continue...")
    m.get_content()
    input("Press Enter to continue...")
    m.show_data()
    input("Press Enter to continue...")
    m.destroy()