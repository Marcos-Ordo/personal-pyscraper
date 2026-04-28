from pathlib import Path
import unittest
import sys

# Si no pongo esto no me trae las librerias
ruta = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta))

from scraper.Maximus import *

class ProductScraperTest(unittest.TestCase):

    def setUp(self):
        self.maximus = MaximusProductScraper(0)
    
    def test001_CuandoElProductScraperDeMaximusBuscaElItem15482_RetornaUnaRTX3050(self):
        self.maximus.id = 15482
        (name, price)   = self.maximus.scrap()
        self.assertEqual(name, "Placa de Video MSI Nvidia Geforce RTX 3050 Ventus 2X 6GB OC GDDR6")
    
    def test002_CuandoElProductScraperDeMaximusBuscaUnItemQueNoEsta_RetornaUnaExcepcion(self):
        with self.assertRaises(Exception):
            self.maximus.scrap()