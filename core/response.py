import uio as io
import uasyncio as asyncio

from microweb.core.fillers.filler_dict import FillerDict
from microweb.core.fillers.filler_string import FillerString
from microweb.core.fillers.filler_textio import FillerTextIO
from microweb.lib.http import HTTPResponseCodes
from microweb.lib.observable import Observable
from microweb.core.logger import logger


class Response:

    app: any
    route: any
    request: any
    http_status: int
    content_type: str
    content_length: int
    on_send: Observable

    def __init__(self, app, writer):
        self.app = app
        self.on_send = Observable()
        self.writer = writer
        self.http_status = 200
        self.content_type = None
        self.content_length = 0
        self.route = None

    def __str__(self):
        return '<response %s %s %s>' % (self.http_status, self.content_type, self.content_length)

    def clear(self):
        del self.app
        del self.on_send
        del self.writer
        del self.http_status
        del self.content_type
        del self.content_length
        del self.route

    def code(self):
        return HTTPResponseCodes[self.http_status][0]

    async def send(self, content: any, status: int = None, ctype: str = None):
        await self._head(status, ctype)
        await self._fill(content, ctype)
        await self._close()

        self._log()
        self._notify()

    async def _head(self, status: int = None, ctype: str = None):
        self.http_status = status if status else self.http_status
        self.content_type = ctype if ctype else self.content_type

        await self.writer.awrite('HTTP/1.1 %s %s\r\n' % (self.http_status, self.code()))
        await self.writer.awrite('Connection: close\r\n')

    async def _fill(self, content, ctype):
        logger.debug('response: content: %s' % content)

        if ctype is None:
            if isinstance(content, str):
                logger.debug('response: detected string filler content')
                filler = FillerString(self)
            elif isinstance(content, dict):
                logger.debug('response: detected dictionary filler content')
                filler = FillerDict(self)
            elif isinstance(content, io.TextIOWrapper):
                logger.debug('response: detected file filler content')
                filler = FillerTextIO(self)
            else:
                logger.debug('response: detected undefined content')
                filler = FillerTextIO(self)
                # filler = None
        else:
            if 'application/json' in ctype:
                filler = FillerDict(self)
            else:
                filler = FillerTextIO(self)

        logger.debug('response: processed using filler: %s' % filler)

        if filler:
            self.content_type, self.content_length = await filler.write(content)
            filler.clear()

    def _log(self):
        route = ('%s %s - ' % (self.route.method, self.route.path)) if self.route else ''
        logger.debug('response: %s - %s%s - %s bytes' % (
            self.http_status, route, self.content_type, self.content_length
        ))

    async def _close(self):
        await self.writer.drain()
        await asyncio.sleep_ms(100)
        await self.writer.aclose()

    def _notify(self):
        self.on_send.fire(self)
