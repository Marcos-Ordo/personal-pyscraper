from abc             import ABC, abstractmethod
from scraper.Scraper import Item, SearchingStrategy

class MaximusSearchingStrategy(SearchingStrategy, ABC):
    def __init__(self, scraper):
        super().__init__(scraper)

    @abstractmethod
    def search(self, msg):
        pass

    # GENERICS
    def generic_search(self, func):
        items = func(1)
        i = 1
        while len(items) > 0:
            for item in items:
                temp = Item({k: item[k] for k in ['item_id','item_desc','prli_price_original']})
                self.scraper.memory.add(temp)
            i += 1
            items = func(i)

    def generic_check_params(self, page, cat, bus):
        params = {
            "page":      page,
            "cat_id":    cat,
            "brand_id":  -1,
            "subcat_id": -1,
            "local":     0,
            "search":    bus,
            "order":     1,
            "price_min": "",
            "price_max": "",
            "wco_tV":    []
        }
        return self.scraper.adapter.request(params)['items']
    
# {"page":1,"cat_id":-1,"brand_id":-1,"search":"ram"}

class MaximusSearchByMessage(MaximusSearchingStrategy):
    def __init__(self, scraper):
        super().__init__(scraper)

    def search(self, msg = None):
        if msg != None:
            self.generic_search(lambda page: self.generic_check_params(page, -1, msg))
        else:
            pass

class MaximusSearchingDefaults(MaximusSearchingStrategy):
    def __init__(self, scraper, category):
        super().__init__(scraper)
        self.__category = category

    @property
    def category(self):
        return self.__category

    def search(self, msg):
        self.generic_search(lambda page: self.generic_check_params(page, self.category, ""))

class MaximusSearchingCPUs(MaximusSearchingDefaults):
    def __init__(self, scraper):
        super().__init__(scraper, 52) # 52 = categoria de las CPUs


class MaximusSearchingGPUs(MaximusSearchingDefaults):
    def __init__(self, scraper):
        super().__init__(scraper, 48) # 48 = categoria de las GPUs