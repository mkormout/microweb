from microweb.core.logger import logger
from microweb.core.middleware import Middleware
from microweb.core.request import Request
from microweb.core.response import Response
from microweb.core.route import Route
from microweb.core.method import Method
from microweb.core.handleable import HandleableContainer, Handler
from microweb.core.buildable import Buildable


class Router(HandleableContainer, Buildable):

    def __init__(self):
        super().__init__()
        self.path = ''
        self.recipe = ''
        self.params = []

    def __str__(self):
        return '<router %s %s>' % (self.path, self.recipe)

    def build(self, path: str = None, start: bool = True, end: bool = True):
        super().build(path=path, end=False)

        node = self.first
        while node:
            node.build(self.path)
            node = node.next

    def use(self, method: Method = None, handler: Handler = None, path: str = None, router: any = None):
        """
        Method registering a middleware function or single route into the request flow.
        Each incoming request is processed through all registered middlewares and routes.
        A single middleware can break request execution process.
        :param (Router) router:
            Router to be registered.
        :param (Method) method:
            HTTP method to specify which requests will be accepted.
        :param (str) path:
            Path prefix associated with given router.
        :param (Handler) handler:
            A function having proper Handler parameters => Request, Response object.
        :return:
            None
        """
        logger.debug('router: using method=%s, path=%s, handler=%s, router=%s' % (method, path, handler, router))

        is_router = router and not (method and path and handler)
        is_middleware = handler and not (method and path)
        is_route = handler and path

        node = None

        if is_router:
            router.path = self.path + path
            router.build()
            node = router

        if is_middleware:
            node = Middleware(handler=handler)

        if is_route:
            node = Route(method=method, path=path, handler=handler)

        if node:
            logger.debug('router: appending %s' % node)
            self.append(node)

    def match(self, request: Request) -> bool:
        if self.pattern:
            match_route = self.pattern.match(request.path)
            return False if match_route is None else True
        else:
            return False

    async def handle(self, request: Request, response: Response) -> bool:

        logger.debug('router: handling %s' % request.path)

        node = self.first

        while node:
            logger.debug('router: testing match with %s' % node)
            if node.match(request):
                logger.debug('router: running handle for %s' % node)
                processing = await node.handle(
                    request,
                    response
                )

                if not processing:
                    logger.debug('router: done execution on %s' % node)
                    return False

            node = node.next

        return True

    def full_path(self):
        parent_path = self.parent.full_path() if self.parent else ''
        return parent_path + self.path

    def delete(self, path: str, handler: Handler):
        """
        Method registering a single DELETE route. Route path supports route params in colon like format.
        :param (str) path:
            Route string.
        :param (Handler) handler:
            Route handler function containing Request and Response parameters.
        :return:
            Route
        """
        return self.use(method=Method.DELETE, path=path, handler=handler)

    def get(self, path: str, handler: Handler):
        """
        Method registering a single GET route. Route path supports route params in colon like format.
        :param (str) path:
            Route string.
        :param (Handler) handler:
            Route handler function containing Request and Response parameters.
        :return:
            Route
        """
        return self.use(method=Method.GET, path=path, handler=handler)

    def put(self, path: str, handler: Handler):
        """
        Method registering a single PUT route. Route path supports route params in colon like format.
        :param (str) path:
            Route string.
        :param (Handler) handler:
            Route handler function containing Request and Response parameters.
        :return:
            Route
        """
        return self.use(method=Method.PUT, path=path, handler=handler)

    def post(self, path: str, handler: Handler):
        """
        Method registering a single POST route. Route path supports route params in colon like format.
        :param (str) path:
            Route string.
        :param (Handler) handler:
            Route handler function containing Request and Response parameters.
        :return:
            Route
        """
        return self.use(method=Method.POST, path=path, handler=handler)

    def patch(self, path: str, handler: Handler):
        """
        Method registering a single PATCH route. Route path supports route params in colon like format.
        :param (str) path:
            Route string.
        :param (Handler) handler:
            Route handler function containing Request and Response parameters.
        :return:
            Route
        """
        return self.use(method=Method.PATCH, path=path, handler=handler)
