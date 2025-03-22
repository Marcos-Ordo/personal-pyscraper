'''
    Target page: https://www.maximus.com.ar/
'''

import Scraper
import csv

'''
Interfaz: get_data(self); get_all(self); redo_data(self); search_for(self,search)
'''

class Maximus(Scraper.Scraper):
    def __init__(self):
        super().__init__("https://www.maximus.com.ar/", True)
        with open('data.csv', mode='a', newline='') as output_file:
            data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_csv.writerow(['Maximus', ''])
            data_csv.writerow(['Artículo', 'Precio'])

    # PROPÓSITO: Recibir la información de @page y guardar esa información en @product_dict.
    # COND: @page debe tener una página.
    def get_data(self):
        super().get_content("product", "title-prod", "price")

    # PROPÓSITO: Recibir toda la información relevante de la solapa donde @page está posicionada. 
    # COND: @page debe tener una página.
    def get_all(self):
        # Preparo el while loop
        i = 1
        super().get_content("product", "title-prod", "price")
        checker = super().check_if_data_exists("product")
        while checker:
            i += 1
            site = self.actual_site[:self.actual_site.rindex("/")-1]+str(i)+"/" # Nasty!
            self.reload_on(site)
            checker = super().check_if_data_exists("product")
            super().get_content("product", "title-prod", "price")

    # PROPÓSITO: borra los datos que ya están en el csv y vuelve a escribir los titulos de la sección.
    def redo_data(self):
        Scraper.delete_data()
        with open('data.csv', mode='w', newline='') as output_file:
            data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_csv.writerow(['Maximus', ''])
            data_csv.writerow(['Artículo', 'Precio'])

    # PROPÓSITO: Buscar !search en la barra de busqueda de la página.
    def search_for(self, search):
        super().search_for(search,"search-input")

    ### IDEA; go_to(): moverme con los botones en la página; pienso que de esa forma no estoy cargando cada página desde 0.


## TESTS ##


def test2():
    # OBJETIVO: Testear "get_all", la busqueda en dos paginas diferentes y el guardado de datos.
    m = Maximus()
    input("Press Enter to continue...")
    m.reload_on("https://www.maximus.com.ar/Productos/Microprocesadores/maximus.aspx?/CAT=52/SCAT=-1/M=-1/OR=1/PAGE=1/")
    input("Press Enter to continue...")
    m.get_all()
    input("Press Enter to continue...")
    m.show_data()
    input("Press Enter to continue...")
    m.search_for("rtx")
    input("Press Enter to continue...")
    m.get_data()
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
    m.reload_on("Micros")
    input("Press Enter to continue...")
    m.get_data()
    input("Press Enter to continue...")
    m.show_data()
    input("Press Enter to continue...")
    m.search_for("rtx")
    input("Press Enter to continue...")
    m.get_data()
    input("Press Enter to continue...")
    m.show_data()
    input("Press Enter to continue...")
    m.destroy()