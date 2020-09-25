import os
from contextlib import ExitStack
from functools import partial

from handlers import AbstractHandler


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
