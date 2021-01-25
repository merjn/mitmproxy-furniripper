from handlers import AbstractHandler
import threading


class ConcurrentHandlerDecorator(AbstractHandler):
    """
    Executes the chain of responsibility concurrently.
    """
    _handler: AbstractHandler

    def __init__(self, handler: AbstractHandler):
        self._handler = handler

    def handle(self, data) -> None:
        p = threading.Thread(target=self._handler.handle, args=(data,))
        p.start()
