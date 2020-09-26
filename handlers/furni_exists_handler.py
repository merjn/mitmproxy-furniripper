import requests

from handlers import AbstractHandler


class FurniExistsHandler(AbstractHandler):
    def handle(self, data) -> None:
        """
        Adds the file name to the data bag if the furniture doesn't exist.

        :param data: the data bag
        :return:
        """
        file_name = self._create_file_name_from_url(data)
        if self._furniture_exists(file_name):
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

    @staticmethod
    def _create_file_name_from_url(data) -> str:
        """
        Extracts the swf file from the url.

        :param data:
        :return:
        """
        return str(data['url']).split('/')[-1]
