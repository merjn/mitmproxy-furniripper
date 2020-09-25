import requests

from handlers import AbstractHandler


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

        print("{} added to catalogue".format(data['file_name']))

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
