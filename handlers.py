from __future__ import annotations
from abc import ABC, abstractmethod
from mitmproxy import ctx
from bs4 import BeautifulSoup
from contextlib import ExitStack
from functools import partial
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
        """
        Adds the file name to the data bag if the furniture doesn't exist.

        :param data: the data bag
        :return:
        """
        file_name = str(data['url']).split('/')[-1]
        if self._furniture_exists(file_name):
            print("Continuing...")
            #ctx.log.info("Furniture {} already exists - continuing...".format(file_name))
            return None

        data['file_name'] = file_name

        return super().handle(data)

    @staticmethod
    def _furniture_exists(file_name: str) -> bool:
        """
        Checks if the furniture already exists.
        :param file_name: furni swf file
        :return:
        """
        request_path = "https://hyrohotel.nl/swf/dcr/hof_furni/{}".format(file_name)
        req = requests.get(request_path)

        return True if req.status_code == 200 else False


class GetFurniMetadataHandler(AbstractHandler):
    def handle(self, data) -> None:
        print("Getting metadata...")
#        ctx.log.info("Getting metadata of {}".format(data['file_name']))

        self._create_swf_file(data)

        with ExitStack() as stack:
            command = "cd binaries/temporary && del {}".format(data['file_name'])
            stack.callback(partial(os.system, command))

            with open("binaries/temporary/{}".format(data['file_name']), 'rb') as f:
                for line in f:
                    codecs.decode(line, 'ascii', errors='ignore')
                    stripped_line = str(line).strip()
                    if "dimensions" in stripped_line:
                        soup = BeautifulSoup(stripped_line, 'html.parser')
                        tag = soup.dimensions

                        # sanity check?
                        attributes = tag.attrs
                        if "x" not in attributes or "y" not in attributes or "z" not in attributes:
                            ctx.log.error("x, y, or z not found in SWF file")
                            return None

                        data['width'] = tag['x']
                        data['length'] = tag['y']
                        data['height'] = tag['z']

                        return super().handle(data)

    @staticmethod
    def _create_swf_file(data):
        f = open("binaries/temporary/{}".format(data['file_name']), 'wb+')
        f.write(data['content'])
        f.flush()
        f.close()

        os.system('cd binaries && swfdecomp.exe ./temporary/{}'.format(data['file_name']))


class GetFurnitureIconHandler(AbstractHandler):
    def handle(self, data) -> None:
        icon_path = data['url'].rsplit("/", 1)[0] + "/icons/"
        icon_file_name = data['file_name'].rsplit(".swf", 1)[0] + "_icon.png"

        data['icon_filename'] = icon_file_name
        data['icon_path'] = icon_path + icon_file_name

        return super().handle(data)


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


class StoreFurnitureHandler(AbstractHandler):
    _session: requests.Session

    def __init__(self, session: requests.Session):
        self._session = session

    def handle(self, data) -> None:
        # Download icon from remote url in order to upload it
        icon_data = self._session.get(data['icon_path']).content

        files = {
            'furniture_file': (data['file_name'], data['content']),
            'furniture_icon_1': (data['icon_filename'], icon_data),
        }

        data = {
            'page_id': '10000100',
            'catalog_name': data['file_name'],
            'cost_credits': '0',
            'cost_points': '75',
            'points_type': '5',
            'amount': '1',
            'song_id': '0',
            'limited_stack': '0',
            'limited_sells': '0',
            'extradata': "",
            'badge': '',
            'club_only': '0',
            'wall-room': "room",
            'type': 's',
            'width': data['width'],
            'length': data['length'],
            'stack_height': data['height'],
            'allow_stack': '1',
            'allow_walk': '0',
            'allow_sit': '0',
            'allow_lay': '0',
            'allow_recycle': '1',
            'allow_trade': '1',
            'allow_marketplace_sell': '1',
            'allow_gift': '1',
            'allow_inventory_stack': '1',
            'interaction_type': 'Default',
            'interaction_modes_count': '2',
            'vending_ids': '0',
            'effect_id_male': '0',
            'effect_id_female': '0',
            'order_number': '0',
            'multiheight': '0'
        }

        response = self._session.post("https://hyrohotel.nl/ase/catalogue/furni/add", files=files, data=data)
        print(response.content)
