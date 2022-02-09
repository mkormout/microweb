from microweb.core.logger import logger

from microweb.core.handleable import HandleableNode, Handler
from microweb.core.request import Request
from microweb.core.response import Response


class Middleware(HandleableNode):

    def __init__(self, handler: Handler):
        super().__init__(handler)

    def __str__(self):
        return '<middleware %s>' % self.handler

    def match(self, request: Request):
        return True

    async def handle(self, request: Request, response: Response):
        logger.debug('handle: running middleware')
        return await self.handler(request, response)
