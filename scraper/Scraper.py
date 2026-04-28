from abc import ABC, abstractmethod

'''
Interfaz: 
    ?
'''

class Scraper(ABC):
    def __init__(self):
        self.__memory = [{}]

    @property
    def memory(self):
        return self.__memory

    @abstractmethod
    def __scrap_product_with_id(self, id) -> tuple[str, str]:
        pass