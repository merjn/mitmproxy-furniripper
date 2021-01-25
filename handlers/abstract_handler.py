from abc import ABC, abstractmethod
from handlers import Handler

class AbstractHandler(Handler):
    _next: Handler = None

    @abstractmethod
    def handle(self, data) -> None:
        if self._next:
            return self._next.handle(data)

    def set_next(self, handler: Handler) -> Handler:
        self._next = handler

        return handler
