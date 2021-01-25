from handlers import AbstractHandler
from mitmproxy import ctx

class FurniIconHandler(AbstractHandler):
    def handle(self, data) -> None:
        icon_path = data['url'].rsplit("/", 1)[0] + "/icons/"
        icon_file_name = data['file_name'].rsplit(".swf", 1)[0] + "_icon.png"

        data['icon_filename'] = icon_file_name
        data['icon_path'] = icon_path + icon_file_name

        ctx.log.info("Icon path {} set".format(data['icon_path']))

        return super().handle(data)
