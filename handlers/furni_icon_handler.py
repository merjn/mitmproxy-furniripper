import requests
from handlers import AbstractHandler
from mitmproxy import ctx


class FurniIconHandler(AbstractHandler):
    def handle(self, data) -> None:
        icon_path = data['url'].rsplit("/", 1)[0] + "/icons/"
        icon_file_name = data['file_name'].rsplit(".swf", 1)[0] + "_icon.png"

        data['icon_name'] = icon_file_name

        # Get content
        icon_content = requests.get(icon_path + icon_file_name)
        if icon_content.status_code != 200:
            ctx.log.error("Unable to get icon content: {} with status code {}".format(icon_content.content, icon_content.status_code))
            return None

        data['icon_content'] = icon_content.content


        ctx.log.info("Icon name {} set".format(data['icon_name']))
        ctx.log.info("Icon content {} set".format(data['icon_content']))
        return super().handle(data)
