from handlers import AbstractHandler
from mitmproxy import ctx
import requests
import base64

class PushFurniToApiHandler(AbstractHandler):
    """
    Pushes the gathered furni data to the server.
    """
    def handle(self, data) -> None:
        payload = {
            'swf_name': data['file_name'],
            'swf_content': base64.b64encode(data['content']),
            'icon_location': data['icon_path'],
            'furni_height': data['height'],
            'furni_width': data['width'],
            'furni_length': data['length']
        }

        # TODO: Get API token
        try:
            response = requests.post("http://localhost:3000/add_furni", data=payload)
            if response.status_code != 200:
                ctx.log.error("Unable to push furni to the server. Error {} occurred with status code {}".format(response.content, response.status_code))
                return None
        except e:
            ctx.log.error("Unable to push furniture to the server. Exception: ")
            ctx.log.error(e)

        return super().handle(data)
