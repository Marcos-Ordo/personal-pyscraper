'''
    target page: https://compragamer.com/
'''

import Scraper
import csv

class Compra(Scraper.Scraper):
    def __init__(self, site = ""):
        super().__init__(site)
        with open('data.csv', mode='a', newline='') as output_file:
            data_csv = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_csv.writerow(['Compragamer', ''])
            data_csv.writerow(['Artículo', 'Precio'])