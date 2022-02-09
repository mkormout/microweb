import ujson as json

from microweb.lib.url import parse_query
from microweb.middleware.body_parser import Parser


class ParserApplicationUrlEncoded(Parser):

    async def read(self):
        data = await self.reader.read(self.length)
        self.request.body = parse_query(str(data))
