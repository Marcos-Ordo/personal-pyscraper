'''
    Target page: https://www.maximus.com.ar/
'''

import Scraper
import csv

class Maximus(Scraper.Scraper):
    def __init__(self, site = "https://www.maximus.com.ar/"):
        super().__init__(site)
        with open('data.csv', mode='a', newline='') as output_file:
            data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_csv.writerow(['Maximus', ''])
            data_csv.writerow(['Artículo', 'Precio'])

    # COND: Needs to have a page loaded.
    def get_data(self):
        content = super().get_content("product")
        for product in content:
            desc = product.find('span', class_="title-prod")
            price = product.find('div', class_="price")
        # Add every description and every price of the products on the page
            if not(desc.text in self.product_dict.keys()) or self.product_dict[desc.text] > price.text:
                self.product_dict[desc.text] = price.text

    def reload_on(self, site):
        match site:
            # Fix this 
            case "Micros": res = "https://www.maximus.com.ar/Productos/Microprocesadores/maximus.aspx?/CAT=52/SCAT=-1/M=-1/OR=1/PAGE=1/"
            case "Placas": res = "https://www.maximus.com.ar/Productos/Placas-De-Video/maximus.aspx?/CAT=48/SCAT=-1/M=-1/OR=1/PAGE=1/"
            case _: res = site
        super().reload_on(res)

    # COND: Needs to have a page loaded.
    def get_all(self):
        # Preparation for while loop
        i = 1
        checker = super().get_content("product")
        self.get_data()
        while checker:
            i += 1
            site = self.actual_site[:self.actual_site.rindex("/")-1]+str(i)+"/" # Nasty!
            self.reload_on(site)
            checker = super().get_content("product")
            self.get_data() 

    def redo_data(self):
        Scraper.delete_data()
        with open('data.csv', mode='w', newline='') as output_file:
            data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_csv.writerow(['Maximus', ''])
            data_csv.writerow(['Artículo', 'Precio'])

    def search_for(self, search):
        super().search_for(search,"search-input")

    '''
        IDEA (GO_TO()):
        CAPAZ HACER CLICK ME AHORRA TENER QUE ESPERAR QUE CARGE TODA LA PAGINA DE NUEVO
    '''

## TESTS ##


def test2():
    # OBJETIVO: Testear "get_all", la busqueda en dos paginas diferentes y el guardado de datos.
    m = Maximus()
    input("Press Enter to continue...")
    m.reload_on("Micros")
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