from __future__ import annotations
from abc import ABC, abstractmethod


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, data):
        pass


class AbstractHandler(Handler):
    _next: Handler = None

    @abstractmethod
    def handle(self, data) -> None:
        if self._next:
            return self._next.handle(data)

    def set_next(self, handler: Handler) -> Handler:
        self._next = handler

        return handler


class FurniExistsHandler(AbstractHandler):
    def handle(self, data) -> None:
        print("validator got", data['url'])
        print("file does not exist, continue...")

        return super().handle(data)


class GetFurniMetadataHandler(AbstractHandler):
    def handle(self, data) -> None:
        print("getting metadata of", data['url'])
