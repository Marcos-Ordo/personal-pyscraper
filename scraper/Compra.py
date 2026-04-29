# target website: https://compragamer.com/

from scraper.Scraper import *

HOME   = "https://www.compragamer.com/"
MICROS = "https://www.compragamer.com/productos?agrup=7"
PLACAS = "https://www.compragamer.com/productos?agrup=2"

class Compra(Scraper):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def changeStratTo(self, strategy):
        pass


