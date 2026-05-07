from flask      import Flask, request, send_from_directory
from flask_cors import CORS
import sys
import os

if getattr(sys, 'frozen', False):
    base = sys._MEIPASS # type: ignore
else:
    base = os.path.abspath(".")

from scraper import *

class Interpreter():
    def __init__(self):
        self.__scrapers: set[Scraper] = set()

    def readAndAdd(self, website):
        if website.lower() not in map(lambda scraper: scraper.name.lower(), self.__scrapers):
            match website.lower():
                case "compragamer": self.__scrapers.add(Compra())
                case "maximus":     self.__scrapers.add(Maximus())
                case _:             pass 

    def handle(self, websites, flags, query, category):
        # Va a intentar agregar un website scraper nuevo al set. Si ya esta no hace nada.
        for website in websites:
            self.readAndAdd(website)

        # No se considera la flag "msg" en caso de haber una categoria, porque esa flag maneja la busqueda de las paginas a las que refieren los mensajes. No tiene sentido decir "Voy a usar CPU y voy a buscar X" porque ese X puede no ser un CPU. (El caso donde quiero traer un CPU con un nombre especifico lo maneja la flag "name", por ejemplo "Quiero todas las GPU con el nombre rtx" trae todas las que incluyan la palabra rtx en su nombre)
        f = lambda scraper: None

        if category != None:
            if category.lower() in ["cpu","gpu"]:
                f = lambda scraper: scraper.change_strat_to(category)

        filters = ANDFilter()

        # Las flags indican que filtros va a usar la query, si no hay flags asumo que no hay query.

        if flags != None:
            for flag in flags:
                match flag:
                    case 'msg':
                        f = lambda scraper: scraper.change_strat_to("msg")
                    case 'name': filters.append(NameFilter())
                    case 'mp':   filters.append(MinimumPriceFilter(request.args.get('mp', type=float)))
                    case 'Mp':   filters.append(MaximumPriceFilter(request.args.get('Mp', type=float)))
        
        for scraper in self.__scrapers:
            f(scraper)
            scraper.search(query, filters)

    def get_memory(self):
        result = []

        for scraper in self.__scrapers:
            for item in scraper.memory.get():
                result.append(item.value)

        return result

app = Flask(__name__, 
            static_folder=os.path.join(base, "website/dist"),
            static_url_path="")
CORS(app)

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html") # type: ignore

@app.route('/products', methods=['GET'])
def products():
    it = Interpreter()

    it.handle(request.args.getlist('websites')
            , request.args.getlist('flags')
            , request.args.get('query', None)
            , None)
    
    return it.get_memory()

@app.route('/products/<category>', methods=['GET'])
def query_products(category):
    it = Interpreter()

    it.handle(request.args.getlist('websites')
            , request.args.getlist('flags')
            , request.args.get('query', None)
            , category)
    
    return it.get_memory()

if __name__ == "__main__":
    app.run()