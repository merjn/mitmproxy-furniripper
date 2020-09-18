from mitmproxy import http
from dispatcher import Dispatcher


class FurnitureInterceptor:
    """
    Intercepts all swf files in the 'hof_furni' directory.
    Note: There's currently no support for different directories.
    """
    _dispatcher: Dispatcher

    _furniture_directory = "hof_furni"
    _desired_file_extension = ".swf"

    def __init__(self, dispatcher: Dispatcher):
        """
        Initializes the event dispatcher.
        :param dispatcher:
        """
        self._dispatcher = dispatcher

    def response(self, flow: http.HTTPFlow) -> None:
        """ Dispatches the content of the response if the response is a valid candidate. """
        if self._is_a_valid_candidate(flow):
            data = {
                'url': flow.request.pretty_url,
                'content': flow.response.get_content(),
            }

            self._dispatcher.dispatch(data)

    def _is_a_valid_candidate(self, flow: http.HTTPFlow) -> bool:
        """ Checks if the current request is a valid candidate. """
        return True if self._furniture_directory in flow.request.pretty_url and self._desired_file_extension in flow.request.pretty_url else False
