import requests

from handlers import AbstractHandler


class HotelAuthenticationHandler(AbstractHandler):
    _session: requests.Session

    def __init__(self, session: requests.Session):
        self._session = session

    def handle(self, data) -> None:
        payload = {
            'loginusername': 'Merijn',
            'loginpassword': 'Kiwi123'
        }

        # TODO: Handle response - this has some special logic because the backend is stupid.
        response = self._session.post("https://hyrohotel.nl/login_submit", data=payload)

        return super().handle(data)

