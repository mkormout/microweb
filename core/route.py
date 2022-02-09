from microweb.core.logger import logger
from microweb.core.handleable import HandleableNode, Handler
from microweb.core.buildable import Buildable
from microweb.core.request import Request
from microweb.core.response import Response
from microweb.core.method import Method


class Route(HandleableNode, Buildable):

    method: Method

    def __init__(self, path: str, handler: Handler, method: Method = None):
        super().__init__(handler)
        self.path = path
        self.method = method
        self.build()

    def __str__(self):
        return '<route %s %s %s>' % (self.method, self.path, self.params)

    def match(self, request: Request) -> bool:
        match_method = not self.method or (self.method == request.method)
        match_route = self.pattern.match(request.path)

        logger.debug('route: match result of %s with %s is %s' % (request.path, self.recipe, match_route))

        if match_route is None:
            match_route = False
        else:
            match_route = True

        match = match_method & match_route

        if match:
            return True

    def prepare(self, request: Request, response: Response):
        request.route = self
        response.route = self

        match = self.pattern.match(request.path)

        for index, param in enumerate(self.params):
            request.params[param] = match.group(index + 1)

        filename = match.group(len(self.params) + 1)

        if filename:
            request.filename = filename[1:]

    async def handle(self, request: Request, response: Response) -> bool:
        logger.debug('route: %s is preparing request %s' % (self, request))
        self.prepare(request, response)
        logger.debug('route: %s is handling request %s' % (self, request))
        await self.handler(request, response)
        logger.debug('route: request handled')
        return False
