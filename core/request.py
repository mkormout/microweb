from microweb.lib.url import parse_path
from microweb.core.method import Method
from microweb.core.logger import logger


class Request:

    app: any
    route: any
    reader: any
    method: Method
    path: str
    proto: str
    params: dict
    query: dict
    headers: dict
    bookmark: str
    filename: str

    def __init__(self, app, reader):
        self.app = app
        self.reader = reader
        self.params = {}
        self.query = {}
        self.headers = {}
        self.method = Method.NONE
        self.path = ''
        self.proto = ''
        self.bookmark = ''
        self.filename = ''

    def __str__(self):
        return '<request %s %s %s>' % (self.method, self.path, self.params)

    def clear(self):
        del self.app
        del self.reader
        del self.params
        del self.query
        del self.headers
        del self.method
        del self.path
        del self.proto
        del self.bookmark
        del self.filename

    async def read(self):
        await self.read_request()
        await self.read_headers()

    async def read_request(self):
        line = await self.reader.readline()

        logger.debug('request: parsing %s' % line)

        line = line.decode()
        self.method, self.path, self.proto = line.split()

        self.path, self.query, self.bookmark = parse_path(self.path)

    async def read_headers(self):
        self.headers = {}
        while True:
            header = await self.reader.readline()
            header = header.decode('utf8')
            if header == '\r\n':
                break
            key, value = header.split(':', 1)
            self.headers[key.lower()] = value.strip()

    def header(self, name: str):
        return self.headers.get(name, None)

