import gc
import micropython
import uasyncio as asyncio

from microweb.core.logger import logger, debug_enabled
from microweb.core.request import Request
from microweb.core.response import Response
from microweb.core.router import Router

gc.threshold(65535)
gc.enable()


class Application(Router):

    def __init__(self):
        super().__init__()

    async def _handle(self, reader, writer):
        """
        Method processing incoming requests. Request and Response objects are created here. This is the place where
        the request flow is beginning. All contained Handleable nodes are being browsed here. Once any of contained
        Handleable is matching incoming route, Handler function is called.
        :param (uasyncio.StreamReader) reader:
            Stream reader object containing a reference to incoming data. Should be parsed into Request object.
        :param (uasyncio.StreamWriter) writer:
            Stream writer object containing a reference to outgoing data. Response object should be prepared.
        :return:
            None
        """
        logger.debug('app: incoming request!')

        request = Request(self, reader)
        response = Response(self, writer)

        await request.read()

        logger.debug('app: request %s: %s ' % (request.method, request.path))

        try:
            try:
                if not await self.handle(request, response):
                    return

                logger.debug('app: %s not found' % request.path)

                # no route found in the loop above? return 404!
                await response.send(status=404, content='404 - "%s" not found' % request.path)
            except Exception as e:
                logger.debug('app: main loop exception')

                if debug_enabled:
                    logger.exc(e=e, msg='app: main loop exception')

                await response.send(status=500, content='500 - "%s" caused exception: "%s"' % (request.path, e))
        finally:
            logger.debug('app: finishing request handle')

            response.clear()
            request.clear()

            del request
            del response

            gc.collect()

            if debug_enabled:
                micropython.mem_info()

    def listen(self, host: str, port: int):
        """
        Method taking care of asynchronous binding of desired port on given host.
        :param (str) host:
            Host name to listen on.
        :param (int) port:
            Port number to listen on.
        :return:
            None
        """
        gc.collect()

        logger.debug('app: getting event loop')
        loop = asyncio.get_event_loop()

        logger.info('app: starting server on ' + str(port))
        loop.create_task(
            asyncio.start_server(self._handle, host, port)
        )

        loop.run_forever()

        logger.debug('app: closing loop')
        loop.close()
