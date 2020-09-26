class Dispatcher:
    _listeners: []

    def __init__(self, listeners):
        self._listeners = listeners

    def dispatch(self, data: any) -> None:
        for listener in self._listeners:
            listener.handle(data)
