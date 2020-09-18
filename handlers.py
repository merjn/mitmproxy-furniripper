from __future__ import annotations
from abc import ABC, abstractmethod
from mitmproxy import ctx
from bs4 import BeautifulSoup
import requests
import os
import codecs


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
        # For now, just perform a request to the site and expect a 200 OK
        file_name = str(data['url']).split('/')[-1]
        request_path = "https://hyrohotel.nl/swf/dcr/hof_furni/{}".format(file_name)
        req = requests.get(request_path)
        if req.status_code == 200:
            ctx.log.info("{} already exists, moving on...".format(file_name))
            return None

        data['file_name'] = file_name

        return super().handle(data)


class GetFurniMetadataHandler(AbstractHandler):
    def handle(self, data) -> None:
        ctx.log.info("Getting metadata of {}".format(data['file_name']))

        f = open("binaries/temporary/{}".format(data['file_name']), 'wb+')
        f.write(data['content'])
        f.flush()
        f.close()

        # Run the SWF decompiler script
        os.system('cd binaries && swfdecomp.exe ./temporary/{}'.format(data['file_name']))

        # Just a very naive heuristic to find the x, y, and z.
        with open("binaries/temporary/{}".format(data['file_name']), 'rb') as f:
            for line in f:
                codecs.decode(line, 'ascii', errors='ignore')
                stripped_line = str(line).strip()
                if "dimensions" in stripped_line:
                    # width (x)
                    # length (y)
                    # height (z)
                    soup = BeautifulSoup(stripped_line, 'html.parser')
                    tag = soup.dimensions

                    # sanity check?
                    attributes = tag.attrs
                    if "x" not in attributes or "y" not in attributes or "z" not in attributes:
                        ctx.log.error("x, y, or z not found in swf file :(")
                        return None

                    data['width'] = tag['x']
                    data['length'] = tag['y']
                    data['height'] = tag['z']

                    return super().handle(data)


class HotelAuthenticationHandler(AbstractHandler):
    def handle(self, data) -> None:
        pass


class StoreFurnitureHandler(AbstractHandler):
    def handle(self, data) -> None:
        pass
