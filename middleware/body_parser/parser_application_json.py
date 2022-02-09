import ujson as json
from microweb.core.logger import logger

from microweb.middleware.body_parser import Parser


class ParserApplicationJSON(Parser):

    async def read(self):
        data = await self.reader.read(self.length)
        logger.debug(data)
        self.request.body = json.loads(data)
