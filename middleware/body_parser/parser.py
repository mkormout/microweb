from microweb.core.request import Request


class Parser:

    request: Request

    def __init__(self, request: Request):
        self.request = request

    def get_reader(self):
        return self.request.reader

    def get_length(self):
        value = self.request.headers['content-length']
        return int(value) if len(value) else 0

    reader = property(get_reader)
    length = property(get_length)

    async def read(self):
        pass

