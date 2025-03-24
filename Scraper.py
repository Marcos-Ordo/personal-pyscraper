from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import os

'''
Interfaz: reload_on(self,site); destroy(self); show_data(self); save_data(self); get_content(self,box,description,price); search_for(self,search,box); delete_data()
'''

class Scraper:
    product_dict = {}
    page_data = [] # [0,1] = Box; [2,3] = Description; [4,5] = Price

    def __init__(self, site, hide_gui: bool):
        self.options = Options()
        if hide_gui:
            # Esconder GUI.
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
    # PARAMS: !site representa una url.
    def reload_on(self, site):
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
    # COND: @page debe tener una página.
    def get_content(self):
        soup = BeautifulSoup(self.page,'lxml')
        print(soup)
        content = soup.find_all(self.page_data[1], class_=self.page_data[0])
        #print(content)
        for product in content:
            desc_prod = product.find(self.page_data[3], class_=self.page_data[2])
            print(desc_prod)
            price_prod = product.find(self.page_data[5], class_=self.page_data[4])
            print(price_prod)
            # Agrega todas las descripciones nuevas junto con los precios de cada producto en @product_dict.
            if not(desc_prod.text in self.product_dict.keys()) or self.product_dict[desc_prod.text] > price_prod.text:
                self.product_dict[desc_prod.text] = price_prod.text

    # PROPÓSITO: Recibir toda la información relevante de la solapa donde @page está posicionada. 
    # COND: @driver debe estar en una página con la información de *button_xpath*.
    # PARAMS:
    # - !button_xpath representa el *xpath* del botón para ir a la siguiente página.
    # - !button_visual_xpath (OPCIONAL) representa el *xpath* de algún elemento previo para que !button_xpath sea visible.
    def get_all(self, button_xpath, button_visual_xpath = None):
        site = self.driver.current_url
        self.get_content()
        self.go_to_next_page(button_xpath, button_visual_xpath)
        while site != self.driver.current_url :
            site = self.driver.current_url
            self.get_content()
            self.go_to_next_page(button_xpath, button_visual_xpath)
            
    # PROPÓSITO: Buscar !search en la barra de busqueda !box.
    # PARAMS: 
    # - !searchbox_xpath representa el *xpath* de la barra de busqueda.
    # - !search representa un string de lo que se quiere buscar.
    def search_for(self, search, searchbox_xpath):
        search_bar = self.driver.find_element(By.XPATH, searchbox_xpath)
        search_bar.send_keys(search)
        search_bar.send_keys(Keys.ENTER)
        try:
            sleep(3)
            self.page = self.driver.page_source
        except TimeoutException:
            print("Page took way to long to load ...")

    # PROPÓSITO: Describe si existe !box y sus elementos.
    # PARAMS: !Box representa el *class name* de un contenedor (div) donde estén todos los productos.
    def check_if_data_exists(self, box):
        try:
            self.driver.find_element(By.CLASS_NAME, box)
        except NoSuchElementException:
            return False
        return True

    # PROPÓSITO: Ir hasta la página siguiente haciendo click en el botón correspondiente.
    # COND: @driver debe estar en una página con un boton para ir a la siguiente.
    # PARAMS:
    # - !button_xpath representa el *xpath* del botón para ir a la siguiente página.
    # - !button_visual_xpath (OPCIONAL) representa el *xpath* de algún elemento previo para que !button_xpath sea visible.
    def go_to_next_page(self, button_xpath: str, button_visual_xpath = None):
        next_page = self.driver.find_element(By.XPATH, button_xpath)
        if button_visual_xpath != None:
            scroll_element = self.driver.find_element(By.XPATH, button_visual_xpath)
            self.driver.execute_script("arguments[0].scrollIntoView();", scroll_element)
        else:
            self.driver.execute_script("arguments[0].scrollIntoView();", next_page)
        sleep(1.5)
        next_page.click()
        sleep(1.5)

# PROPÓSITO: borrar el csv.
def delete_data():
        os.remove('data.csv')