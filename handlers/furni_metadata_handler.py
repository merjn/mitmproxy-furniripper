import codecs
import os
import base64
from contextlib import ExitStack
from functools import partial
from mitmproxy import ctx
from handlers import AbstractHandler
from bs4 import BeautifulSoup

class FurniMetadataHandler(AbstractHandler):
    def handle(self, data) -> None:
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

                        attributes = tag.attrs
                        if "x" not in attributes or "y" not in attributes or "z" not in attributes:
                            ctx.log.error("x, y, or z not found in SWF file")
                            return None

                        data['width'] = tag['x']
                        data['length'] = tag['y']
                        data['height'] = tag['z']

                        ctx.log.info("Found furniture width (x): {}".format(tag['x']))
                        ctx.log.info("Found furniture length (y): {}".format(tag['y']))
                        ctx.log.info("Found furniture height (z): {}".format(tag['z']))

                return super().handle(data)

    @staticmethod
    def _create_swf_file(data):
        f = open("binaries/temporary/{}".format(data['file_name']), 'wb+')
        f.write(data['content'])
        f.flush()
        f.close()

        os.system('cd binaries && swfdecomp.exe ./temporary/{}'.format(data['file_name']))
