from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import csv
import os

class Scraper:
    product_dict = {}

    def __init__(self, site):
        # Save the site inserted
        self.actual_site = site
        # hide GUI
        self.options = Options()
        self.options.add_argument("-headless")
        # Avoid loading images
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        self.options.profile = firefox_profile
        self.driver = webdriver.Firefox(options=self.options)
        # Load the webpage
        self.driver.get(site)
        self.page = self.driver.page_source

    def reload_on(self, site):
        self.actual_site = site
        self.driver.get(site)
        sleep(3)
        self.page = self.driver.page_source

    def destroy(self):
        self.driver.close()

    # COND: Needs to have data loaded.
    def show_data(self):
        print(self.product_dict)

    # COND: Needs to have data loaded.
    def save_data(self):
        with open('data.csv', mode='a', newline='') as output_file:
            data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for key in self.product_dict:
                data_csv.writerow([key, self.product_dict[key]])

    # COND: Box need's to be a container (div) and the class name of all the elements to get the content from
    def get_content(self, box):
        soup = BeautifulSoup(self.page,'lxml')
        content = soup.find_all('div', class_=box)
        return content

    # COND: Box need's to be a class name
    def search_for(self, search, box):
        search_bar = self.driver.find_element(By.CLASS_NAME, box)
        search_bar.send_keys(search)
        search_bar.send_keys(Keys.ENTER)
        try:
            #WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'product')))
            sleep(3)
            self.page = self.driver.page_source
        except TimeoutException:
            print("Page took way to long to load ...")

def delete_data():
        os.remove('data.csv')