from microweb.core.request import Request
from microweb.core.response import Response


async def request_dump(request: Request, response: Response):
    print('+--------------------------------------')
    print('| Request Dump: %s %s %s' % (request.method, request.path, request.proto))
    print('+--------------------------------------')

    for (key, value) in request.headers.items():
        print('| %s: %s' % (key, value))

    print('+--------------------------------------')

    return True

