import gc
import os
import uio as io

from microweb.core.request import Request
from microweb.core.response import Response
from microweb.core.router import Router
from microweb.core.logger import logger, debug_enabled
from microweb.lib.http import filename_mime


class Static(Router):
    root: str
    options: dict

    def __init__(self, root: str, options: dict = None):
        super().__init__()
        self.root = root
        self.options = options

    def __str__(self):
        return '<static %s => %s>' % (self.path, self.root)

    async def handle(self, request: Request, response: Response) -> bool:
        filename = request.path

        logger.debug('static: replacing %s with %s' % (self.full_path(), self.root))

        path = filename.replace(
            self.full_path(),
            self.root + '/',
            1
        )

        try:
            gc.collect()

            logger.debug('static: opening file: %s' % path)
            file = open(path)

            logger.debug('static: getting mime')
            mime = filename_mime(path)

            logger.debug('static: sending response: %s' % file)
            await response.send(content=file, ctype=mime)

            logger.debug('static: closing file')
            file.close()

            return False
        except Exception as e:
            logger.debug('static: error reading file: %s' % e)

            return True
