from pathlib import Path
import unittest
from unittest.mock import MagicMock
import sys

# Si no pongo esto no me trae las librerias
ruta = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta))

from scraper.maximus.Maximus import MaximusProductScraper, MaximusAdapter

class ProductScraperTest(unittest.TestCase):

    def setUp(self):
        self.adapter = MaximusAdapter()
        self.maximus = MaximusProductScraper(self.adapter)
    
    def test001_CuandoElProductScraperDeMaximusBuscaElItem15482_RetornaUnaRTX3050(self):
        self.adapter.request = MagicMock(return_value = ("Placa de Video MSI Nvidia Geforce RTX 3050 Ventus 2X 6GB OC GDDR6", 0))

        (name, price)   = self.maximus.scrap(15482)
        self.assertEqual(name, "Placa de Video MSI Nvidia Geforce RTX 3050 Ventus 2X 6GB OC GDDR6")
    
    def test002_CuandoElProductScraperDeMaximusBuscaUnItemQueNoEsta_RetornaUnaExcepcion(self):
        self.adapter.request = MagicMock(side_effect = Exception)

        with self.assertRaises(Exception):
            self.maximus.scrap(0)

if __name__ == "__main__":
    unittest.main()