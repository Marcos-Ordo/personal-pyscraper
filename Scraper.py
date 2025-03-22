from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import csv
import os

'''
Interfaz: reload_on(self,site); destroy(self); show_data(self); save_data(self); get_content(self,box,description,price); search_for(self,search,box); delete_data()
'''

class Scraper:
    product_dict = {}

    def __init__(self, site, hide_gui: bool):
        # Guardar el sitio.
        self.actual_site = site
        if hide_gui:
            # Esconder GUI.
            self.options = Options()
            self.options.add_argument("-headless")
        # Evitar la carga de imágenes.
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        self.options.profile = firefox_profile
        self.driver = webdriver.Firefox(options=self.options)
        # Cargar la página.
        self.driver.get(site)
        self.page = self.driver.page_source

    # PROPÓSITO: Recargar la instancia de la página en !site.
    # COND: !page debe ser una url.
    def reload_on(self, site):
        self.actual_site = site
        self.driver.get(site)
        sleep(3)
        self.page = self.driver.page_source

    # PROPÓSITO: Destruir la instancia de la página.
    def destroy(self):
        self.driver.close()

    # PROPÓSITO: Mostar los datos que tiene guardados @product_dict.
    def show_data(self):
        print(self.product_dict)

    # PROPÓSITO: Guardar la información recibida en el csv.
    def save_data(self):
        with open('data.csv', mode='a', newline='') as output_file:
            data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for key in self.product_dict:
                data_csv.writerow([key, self.product_dict[key]])

    # PROPÓSITO: Recibir la información de @page y guardar esa información en @product_dict.
    # COND: 
    # - !Box debe ser el *class name* de un contenedor (div) donde estén todos los productos.
    # - !description debe ser el *class name* de los elementos que poseen la descripción del producto.
    # - !price debe ser el *class name* de los elementos que poseen el precio del producto.
    def get_content(self, box, description, price):
        soup = BeautifulSoup(self.page,'lxml')
        content = soup.find_all('div', class_=box)
        for product in content:
            desc_prod = product.find('span', class_=description)
            price_prod = product.find('div', class_=price)
            # Agrega todas las descripciones nuevas junto con los precios de cada producto en @product_dict.
            if not(desc_prod.text in self.product_dict.keys()) or self.product_dict[desc_prod.text] > price_prod.text:
                self.product_dict[desc_prod.text] = price_prod.text

    # PROPÓSITO: Buscar !search en la barra de busqueda !box.
    # COND: 
    # - !Box debe ser el *class name* de la barra de busqueda.
    # - !search debe ser un string con lo que se quiere buscar.
    def search_for(self, search, box):
        search_bar = self.driver.find_element(By.CLASS_NAME, box)
        search_bar.send_keys(search)
        search_bar.send_keys(Keys.ENTER)
        try:
            sleep(3)
            self.page = self.driver.page_source
        except TimeoutException:
            print("Page took way to long to load ...")

# PROPÓSITO: borrar el csv.
def delete_data():
        os.remove('data.csv')