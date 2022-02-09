from microweb.core.logger import logger
from microweb.core.request import Request
from microweb.core.response import Response
from microweb.middleware.body_parser.parser import Parser
from microweb.middleware.body_parser.parser_application_json import ParserApplicationJSON
from microweb.middleware.body_parser.parser_application_urlencoded import ParserApplicationUrlEncoded


def get_parser(request: Request):
    try:
        header = request.header('content-type')

        if header == 'application/json':
            return ParserApplicationJSON(request)

        if header == 'application/x-www-form-urlencoded':
            return ParserApplicationUrlEncoded(request)

    except KeyError as e:
        return None


async def body_parser(request: Request, response: Response):
    logger.debug('body_parser middleware: enter %s' % request)

    parser = get_parser(request)

    logger.debug('body_parser middleware: using parser %s' % parser)

    if parser:
        logger.debug('body_parser middleware: reading %s' % parser)
        await parser.read()
    else:
        logger.debug('body_parser no suitable parser for %s' % request.header('content-type'))

    return True
