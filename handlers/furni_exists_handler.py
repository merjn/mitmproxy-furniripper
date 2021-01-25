from handlers import AbstractHandler
from mitmproxy import ctx
import requests

class FurniExistsHandler(AbstractHandler):
    """
    Checks if a file already exists on the remote server.
    """

    def handle(self, data) -> None:
        """
        Adds the file name to the data bag if the furniture does not exist.
        """
        file_name = self._create_file_name_from_url(data)
        if self._furniture_exists(file_name):
            ctx.log.info("Furni {} already exists".format(file_name))
            return None

        ctx.log.info("Furni {} added to queue".format(file_name))
        data['file_name'] = file_name

        return super().handle(data)

    @staticmethod
    def _furniture_exists(file_name: str) -> bool:
        """
        Checks if the furniture already exists.

        :param file_name: furni swf file
        :return:
        """
        request_path = "https://swfs.habbo.ovh/dcr/hof_furni/{}".format(file_name)
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
