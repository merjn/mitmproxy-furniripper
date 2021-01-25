from handlers import AbstractHandler


class SetFileNameHandler(AbstractHandler):
    """
    Stores the swf file name to the data bag.

    It extracts it from the url, because that contains the file name.
    """
    def handle(self, data) -> None:
        file_name = str(data['url']).split('/')[-1]
        if file_name == "":
            return None

        data['file_name'] = file_name

        return super().handle(data)
