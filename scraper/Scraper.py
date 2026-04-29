from abc import ABC, abstractmethod

class Scraper(ABC):
    '''
    Esta clase abstracta define la propiedad de la memoria de un scraper y define la siguiente interfaz: 
        * search_gpus: Una funcion que debe ser capaz de scrapear todas las gpus de la "target website".
        * search_cpus: Una funcion que debe ser capaz de scrapear todas las cpus de la "target website".
    '''
    def __init__(self):
        self.__memory = set()

    @property
    def memory(self):
        return self.__memory

    @abstractmethod
    def search_gpus(self):
        pass

    @abstractmethod
    def search_cpus(self):
        pass

class ById:
    """
    Este wrapper lo hice para que 2 items puedan compararse por igualdad, asi pueda ponerlos de forma segura en un set.
    Es una clase sin metodos, solo tiene propiedades.
    """
    def __init__(self, value):
        self.__value = value

    def __eq__(self, other):
        if not isinstance(other, ById):
            return False
        return self.__value['item_id'] == other.__value['item_id']

    def __hash__(self):
        return hash(self.__value['item_id'])

    def __repr__(self):
        return f"ById({self.__value})"
    
    @property
    def value(self):
        return self.__value