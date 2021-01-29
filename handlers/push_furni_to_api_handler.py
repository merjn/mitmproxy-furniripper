from handlers import AbstractHandler
from mitmproxy import ctx
import requests
import base64
import os

class PushFurniToApiHandler(AbstractHandler):
    """
    Pushes the gathered furni data to the server.
    """
    def handle(self, data) -> None:
        payload = {
            'swf_name': data['file_name'],
            'swf_content': base64.b64encode(data['content']),
            'icon_name': data['icon_name'],
            'icon_content': base64.b64encode(data['icon_content']),
            'furni_height': data['height'],
            'furni_width': data['width'],
            'furni_length': data['length']
        }

        headers = {
            "Authorization": "Bearer {}".format(os.environ.get('FURNIRIPPER_AUTH_TOKEN'))
        }
        try:
            response = requests.post("http://localhost:3000/add_furni", data=payload, headers=headers)
            if response.status_code != 200:
                ctx.log.error("Unable to push furni to the server. Error {} occurred with status code {}".format(response.content, response.status_code))
                return None
        except Exception as e:
            ctx.log.error("Unable to push furniture to the server. Exception: ")
            ctx.log.error(e)

        return super().handle(data)
