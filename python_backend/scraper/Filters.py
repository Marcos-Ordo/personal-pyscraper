from abc import ABC, abstractmethod

## TODO! finish implementing filters!!

class Filter(ABC):
    def __init__(self):
        pass


class NameFilter(Filter):
    def __init__(self):
        super().__init__()


class MinimumPriceFilter(Filter):
    def __init__(self, num):
        super().__init__()


class MaximumPriceFilter(Filter):
    def __init__(self, num):
        super().__init__()


class ANDFilter(Filter):
    def __init__(self):
        self.__filters = []
        super().__init__()

    def append(self, filter):
        self.__filters.append(filter)
