from abc import ABC, abstractmethod


class Store(ABC):
    @abstractmethod
    def add_furniture(self):
        """ Adds furniture to the catalogue. """
        pass

    @abstractmethod
    def create_catalogue_category(self):
        """ Adds a new category to the catalogue. """
        pass
