from pathlib import Path
import unittest
from unittest.mock import MagicMock
import sys
import json

# Si no pongo esto no me trae las librerias
ruta = Path(__file__).resolve().parent.parent
sys.path.append(str(ruta))

from scraper.maximus.Maximus import MaximusAdapter

class ProductScraperTest(unittest.TestCase):

    def setUp(self):
        self.adapter  = MaximusAdapter()
        self.session  = MagicMock()
        self.response = MagicMock()
        self.cookie0  = MagicMock()

        self.cookies      = []
        self.cookie0.name = "GBP_123"
    
    def test001_CuandoElAdapterIntentaHacerUnaRequestYPuede_RetornaUnaRespuesta(self):
        self.cookies.append(self.cookie0)
        self.session.cookies           = self.cookies
        self.session.post.return_value = self.response
        self.response.status_code      = 200
        self.response.text             = json.dumps({"d": json.dumps({"data": "Success"})})

        self.assertEqual(self.adapter.request({}, self.session), "Success")

    def test002_CuandoElAdapterIntentaHacerUnaRequestYPuedePeroElJSonCambia_RetornaNone(self):
        self.cookies.append(self.cookie0)
        self.session.cookies           = self.cookies
        self.session.post.return_value = self.response
        self.response.status_code      = 200
        self.response.text             = json.dumps({"a": "bcd"})

        self.assertEqual(self.adapter.request({}, self.session), None)

    def test003_CuandoElAdapterIntentaHacerUnaRequestYNoPuedePorLasCookies_RetornaUnaExcepcion(self):
        self.session.cookies = self.cookies

        with self.assertRaises(Exception):
            self.adapter.request({}, self.session)

    def test004_CuandoElAdapterIntentaHacerUnaRequestYNoPuedePorLaConexion_RetornaUnaExcepcion(self):
        self.cookies.append(self.cookie0)
        self.session.cookies = self.cookies
        self.session.post.return_value = self.response
        self.response.status_code = 500

        with self.assertRaises(Exception):
            self.adapter.request({}, self.session)


if __name__ == "__main__":
    unittest.main()