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
        self.adapter = MagicMock()
        self.maximus = MaximusProductScraper(self.adapter)
    
    def test001_CuandoElProductScraperDeMaximusBuscaElItem15482_RetornaUnaRTX3050(self):
        self.adapter.request.return_value = {'item_desc': "Placa de Video MSI Nvidia Geforce RTX 3050 Ventus 2X 6GB OC GDDR6"}

        item = self.maximus.scrap(15482)
        self.assertEqual(item.value['item_desc'], "Placa de Video MSI Nvidia Geforce RTX 3050 Ventus 2X 6GB OC GDDR6") # type: ignore
    
    def test002_CuandoElProductScraperDeMaximusBuscaUnItemQueNoEsta_RetornaNone(self):
        self.adapter.request.return_value = None

        self.assertEqual(self.maximus.scrap(15482), None)

if __name__ == "__main__":
    unittest.main()